package main

import (
	"bytes"
	"crypto/rand"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"fmt"
	"hash"
	"io"
	"net"
	"sync"
)

// 协议中使用的消息类型
const (
	MessageTypeData byte = 1 // 普通数据消息
	MessageTypeEOF  byte = 2 // EOF结束标记
)

// Conn 表示实现了一个简单的基于TCP的协议的连接
// 支持基于键的数据传输和EOF检测
type Conn struct {
	netConn   net.Conn
	isClosed  bool

	// 用于支持EOF检测的缓冲区
	dataBuffer *bytes.Buffer
}

// NewConn 创建一个新的协议连接，包装标准的net.Conn
func NewConn(netConn net.Conn) *Conn {
	return &Conn{
		netConn:    netConn,
		dataBuffer: new(bytes.Buffer),
	}
}

// DataWriter 处理特定键的数据写入
type DataWriter struct {
	parentConn *Conn
	isClosed   bool
}

// Send 开始发送由给定键标识的数据
// 返回一个可用于分多次发送数据块的写入器
// 数据全部写入后，调用者应关闭写入器以表示完成
func (conn *Conn) Send(key string) (writer io.WriteCloser, err error) {
	fmt.Println("开始发送操作")

	// 准备键信息
	keyBytes := []byte(key)
	keyLength := uint32(len(keyBytes))

	// 创建键头部的缓冲区
	headerBuffer := new(bytes.Buffer)

	// 写入键长度（4字节）
	if err := binary.Write(headerBuffer, binary.BigEndian, keyLength); err != nil {
		return nil, fmt.Errorf("编码键长度失败: %w", err)
	}

	// 写入键内容
	if _, err := headerBuffer.Write(keyBytes); err != nil {
		return nil, fmt.Errorf("写入键数据失败: %w", err)
	}

	// 通过连接发送键信息
	if _, err := conn.netConn.Write(headerBuffer.Bytes()); err != nil {
		return nil, fmt.Errorf("发送键头部失败: %w", err)
	}

	fmt.Println("键发送成功")
	return &DataWriter{parentConn: conn}, nil
}

// Write 通过连接发送一块数据
// 格式：[消息类型(1字节)][数据长度(4字节)][数据(可变)]
func (writer *DataWriter) Write(dataChunk []byte) (bytesWritten int, err error) {
	if writer.isClosed {
		return 0, fmt.Errorf("无法写入已关闭的写入器")
	}

	// 创建数据包的缓冲区
	packetBuffer := new(bytes.Buffer)

	// 写入消息类型（数据包）
	if err := packetBuffer.WriteByte(MessageTypeData); err != nil {
		return 0, fmt.Errorf("写入消息类型失败: %w", err)
	}

	// 写入数据长度
	dataLength := uint32(len(dataChunk))
	if err := binary.Write(packetBuffer, binary.BigEndian, dataLength); err != nil {
		return 0, fmt.Errorf("编码数据长度失败: %w", err)
	}

	// 写入实际数据
	if _, err := packetBuffer.Write(dataChunk); err != nil {
		return 0, fmt.Errorf("写入数据块失败: %w", err)
	}

	// 发送完整的数据包
	if _, err := writer.parentConn.netConn.Write(packetBuffer.Bytes()); err != nil {
		return 0, fmt.Errorf("发送数据包失败: %w", err)
	}

	return len(dataChunk), nil
}

// Close 表示此键的所有数据已传输完毕
// 这只关闭数据流，不关闭底层连接
func (writer *DataWriter) Close() error {
	if writer.isClosed {
		return fmt.Errorf("写入器已经关闭")
	}

	writer.isClosed = true

	// 创建EOF数据包：[消息类型(1字节)][长度(4字节)=0]
	eofBuffer := new(bytes.Buffer)

	// 写入EOF消息类型
	if err := eofBuffer.WriteByte(MessageTypeEOF); err != nil {
		return fmt.Errorf("写入EOF标记类型失败: %w", err)
	}

	// 写入零长度
	if err := binary.Write(eofBuffer, binary.BigEndian, uint32(0)); err != nil {
		return fmt.Errorf("写入EOF标记长度失败: %w", err)
	}

	// 发送EOF数据包
	if _, err := writer.parentConn.netConn.Write(eofBuffer.Bytes()); err != nil {
		return fmt.Errorf("发送EOF标记失败: %w", err)
	}

	fmt.Println("数据传输完成，已发送EOF标记")
	return nil
}

// Receive 准备接收由键标识的数据
// 返回键和用于访问接收数据的读取器
// 当读取器返回io.EOF时，表示此键的所有数据已接收完毕
func (conn *Conn) Receive() (key string, reader io.Reader, err error) {
	fmt.Println("开始接收操作")

	// 读取键长度（4字节）
	var keyLength uint32
	if err := binary.Read(conn.netConn, binary.BigEndian, &keyLength); err != nil {
		if err == io.EOF {
			return "", nil, io.EOF
		}
		return "", nil, fmt.Errorf("读取键长度失败: %w", err)
	}

	fmt.Printf("收到键长度: %d字节\n", keyLength)

	// 读取键内容
	keyBytes := make([]byte, keyLength)
	if _, err := io.ReadFull(conn.netConn, keyBytes); err != nil {
		return "", nil, fmt.Errorf("读取键内容失败: %w", err)
	}

	key = string(keyBytes)
	fmt.Printf("收到键: %s\n", key)

	// 返回处理协议细节的自定义读取器
	return key, &DataReader{
		parentConn:    conn,
		hasReachedEOF: false,
		pendingData:   nil,
	}, nil
}

// DataReader 处理特定键的数据读取
type DataReader struct {
	parentConn    *Conn
	hasReachedEOF bool
	pendingData   []byte  // 存储已读取但尚未返回的数据
}

// Read 实现io.Reader接口以处理特定协议的数据读取
func (reader *DataReader) Read(dataBuffer []byte) (bytesRead int, err error) {
	// 如果我们在之前的读取中已达到EOF，直接返回EOF
	if reader.hasReachedEOF {
		return 0, io.EOF
	}

	// 如果我们有上次读取剩余的数据，先返回它
	if len(reader.pendingData) > 0 {
		bytesRead = copy(dataBuffer, reader.pendingData)
		reader.pendingData = reader.pendingData[bytesRead:]
		return bytesRead, nil
	}

	// 读取消息类型（1字节）
	typeBuffer := make([]byte, 1)
	if _, err = io.ReadFull(reader.parentConn.netConn, typeBuffer); err != nil {
		if err == io.EOF {
			reader.hasReachedEOF = true
		}
		return 0, err
	}

	// 读取数据长度（4字节）
	var dataLength uint32
	if err = binary.Read(reader.parentConn.netConn, binary.BigEndian, &dataLength); err != nil {
		return 0, fmt.Errorf("读取数据长度失败: %w", err)
	}

	// 根据消息类型处理
	messageType := typeBuffer[0]
	switch messageType {
	case MessageTypeEOF:
		// 我们收到了EOF标记
		reader.hasReachedEOF = true
		return 0, io.EOF

	case MessageTypeData:
		// 我们收到了数据包
		if dataLength == 0 {
			return 0, nil
		}

		// 读取实际数据
		receivedData := make([]byte, dataLength)
		if _, err = io.ReadFull(reader.parentConn.netConn, receivedData); err != nil {
			return 0, fmt.Errorf("读取消息数据失败: %w", err)
		}

		// 将数据复制到输出缓冲区
		bytesRead = copy(dataBuffer, receivedData)

		// 如果我们无法将所有数据放入输出缓冲区，存储剩余部分供以后使用
		if bytesRead < len(receivedData) {
			reader.pendingData = receivedData[bytesRead:]
		}

		return bytesRead, nil

	default:
		return 0, fmt.Errorf("未知的消息类型: %d", messageType)
	}
}

// Close 关闭底层网络连接
func (conn *Conn) Close() {
	if !conn.isClosed {
		conn.isClosed = true
		conn.netConn.Close()
		fmt.Println("连接已关闭")
	}
}

//##########################################################
//################### TEST CASE START HERE #################
//##########################################################
// 连接到测试服务器，获得一个你实现的连接对象
func dial(serverAddr string) *Conn {
	conn, err := net.Dial("tcp", serverAddr)
	if err != nil {
		panic(err)
	}
	return NewConn(conn)
}

// 启动测试服务器
func startServer(handle func(*Conn)) net.Listener {
	ln, err := net.Listen("tcp", ":0")
	if err != nil {
		panic(err)
	}
	go func() {
		for {
			conn, err := ln.Accept()
			if err != nil {
				fmt.Println("[WARNING] ln.Accept", err)
				return
			}
			go handle(NewConn(conn))
		}
	}()
	return ln
}

// 简单断言
func assertEqual[T comparable](actual T, expected T) {
	if actual != expected {
		panic(fmt.Sprintf("actual:%v expected:%v\n", actual, expected))
	}
}

// 简单 case：单连接，双向传输少量数据
func testCase0() {
	const (
		key  = "Bible"
		data = `Then I heard the voice of the Lord saying, “Whom shall I send? And who will go for us?”
And I said, “Here am I. Send me!”
Isaiah 6:8`
	)
	ln := startServer(func(conn *Conn) {
		// 服务端等待客户端进行传输
		_key, reader, err := conn.Receive()
		if err != nil {
			panic(err)
		}
		assertEqual(_key, key)
		dataB, err := io.ReadAll(reader)
		if err != nil {
			panic(err)
		}
		assertEqual(string(dataB), data)

		// 服务端向客户端进行传输
		writer, err := conn.Send(key)
		if err != nil {
			panic(err)
		}
		n, err := writer.Write([]byte(data))
		if err != nil {
			panic(err)
		}
		if n != len(data) {
			panic(n)
		}
		conn.Close()
	})
	//goland:noinspection GoUnhandledErrorResult
	defer ln.Close()

	conn := dial(ln.Addr().String())
	// 客户端向服务端传输
	writer, err := conn.Send(key)
	if err != nil {
		panic(err)
	}
	n, err := writer.Write([]byte(data))
	if n != len(data) {
		panic(n)
	}
	err = writer.Close()
	if err != nil {
		panic(err)
	}
	// 客户端等待服务端传输
	_key, reader, err := conn.Receive()
	if err != nil {
		panic(err)
	}
	assertEqual(_key, key)
	dataB, err := io.ReadAll(reader)
	if err != nil {
		panic(err)
	}
	assertEqual(string(dataB), data)
	conn.Close()
}

// 生成一个随机 key
func newRandomKey() string {
	buf := make([]byte, 8)
	_, err := rand.Read(buf)
	if err != nil {
		panic(err)
	}
	return hex.EncodeToString(buf)
}

// 读取随机数据，并返回随机数据的校验和：用于验证数据是否完整传输
func readRandomData(reader io.Reader, hash hash.Hash) (checksum string) {
	hash.Reset()
	var buf = make([]byte, 23<<20) //调用者读取时的 buf 大小不是固定的，你的实现中不可假定 buf 为固定值
	for {
		n, err := reader.Read(buf)
		if err == io.EOF {
			break
		}
		if err != nil {
			panic(err)
		}
		_, err = hash.Write(buf[:n])
		if err != nil {
			panic(err)
		}
	}
	checksum = hex.EncodeToString(hash.Sum(nil))
	return checksum
}

// 写入随机数据，并返回随机数据的校验和：用于验证数据是否完整传输
func writeRandomData(writer io.Writer, hash hash.Hash) (checksum string) {
	hash.Reset()
	const (
		dataSize = 500 << 20 //一个 key 对应 500MB 随机二进制数据，dataSize 也可以是其他值，你的实现中不可假定 dataSize 为固定值
		bufSize  = 1 << 20   //调用者写入时的 buf 大小不是固定的，你的实现中不可假定 buf 为固定值
	)
	var (
		buf  = make([]byte, bufSize)
		size = 0
	)
	for i := 0; i < dataSize/bufSize; i++ {
		_, err := rand.Read(buf)
		if err != nil {
			panic(err)
		}
		_, err = hash.Write(buf)
		if err != nil {
			panic(err)
		}
		n, err := writer.Write(buf)
		if err != nil {
			panic(err)
		}
		size += n
	}
	if size != dataSize {
		panic(size)
	}
	checksum = hex.EncodeToString(hash.Sum(nil))
	return checksum
}

// 复杂 case：多连接，双向传输，大量数据，多个不同的 key
func testCase1() {
	var (
		mapKeyToChecksum = map[string]string{}
		lock             sync.Mutex
	)
	ln := startServer(func(conn *Conn) {
		// 服务端等待客户端进行传输
		key, reader, err := conn.Receive()
		if err != nil {
			panic(err)
		}
		var (
			h         = sha256.New()
			_checksum = readRandomData(reader, h)
		)
		lock.Lock()
		checksum, keyExist := mapKeyToChecksum[key]
		lock.Unlock()
		if !keyExist {
			panic(fmt.Sprintln(key, "not exist"))
		}
		assertEqual(_checksum, checksum)

		// 服务端向客户端连续进行 2 次传输
		for _, key := range []string{newRandomKey(), newRandomKey()} {
			writer, err := conn.Send(key)
			if err != nil {
				panic(err)
			}
			checksum := writeRandomData(writer, h)
			lock.Lock()
			mapKeyToChecksum[key] = checksum
			lock.Unlock()
			err = writer.Close() //表明该 key 的所有数据已传输完毕
			if err != nil {
				panic(err)
			}
		}
		conn.Close()
	})
	//goland:noinspection GoUnhandledErrorResult
	defer ln.Close()

	conn := dial(ln.Addr().String())
	// 客户端向服务端传输
	var (
		key = newRandomKey()
		h   = sha256.New()
	)
	writer, err := conn.Send(key)
	if err != nil {
		panic(err)
	}
	checksum := writeRandomData(writer, h)
	lock.Lock()
	mapKeyToChecksum[key] = checksum
	lock.Unlock()
	err = writer.Close()
	if err != nil {
		panic(err)
	}

	// 客户端等待服务端的多次传输
	keyCount := 0
	for {
		key, reader, err := conn.Receive()
		if err == io.EOF {
			// 服务端所有的数据均传输完毕，关闭连接
			break
		}
		if err != nil {
			panic(err)
		}
		_checksum := readRandomData(reader, h)
		lock.Lock()
		checksum, keyExist := mapKeyToChecksum[key]
		lock.Unlock()
		if !keyExist {
			panic(fmt.Sprintln(key, "not exist"))
		}
		assertEqual(_checksum, checksum)
		keyCount++
	}
	assertEqual(keyCount, 2)
	conn.Close()
}

func main() {
	testCase0()
	testCase1()
}
