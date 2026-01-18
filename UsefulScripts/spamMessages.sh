#!/bin/bash

# 发送4096条消息到RabbitMQ - 并发版本

TOTAL_MESSAGES=4096
RABBITMQ_USER="YOUR-USERNAME-HERE"
RABBITMQ_PASS="YOUR-PASSWORD-HERE"
RABBITMQ_URL="http://localhost:15681/api/exchanges/%2f/amq.direct/publish"
ROUTING_KEY="test_queue"
MAX_PARALLEL=20  # 最大并发数

echo "开始并发发送 $TOTAL_MESSAGES 条消息..."

send_message() {
    local i=$1
    TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    PAYLOAD=$(printf '{"message":"

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam volutpat arcu nisl, a varius turpis consequat id. Phasellus eleifend purus id rutrum vestibulum. Fusce ultricies sem at tincidunt interdum. Nullam sit amet leo eros. Ut eget massa sit amet urna tincidunt faucibus in quis ex. Morbi sed nisl vitae tortor vestibulum aliquam at non magna. Cras id congue felis. Suspendisse porttitor sodales erat, eget viverra enim egestas sit amet. Morbi in justo vitae leo aliquet auctor. Donec massa nisi, vestibulum sed ligula ac, egestas fringilla nulla. Etiam lacinia eleifend ipsum eget egestas. Sed lacinia semper massa laoreet malesuada. Sed ac justo nulla. Proin dui nisi, rutrum sed massa finibus, auctor congue nibh. Mauris porttitor, dui a finibus sodales, leo purus feugiat dolor, eget volutpat nisi velit non nulla. Duis vitae ornare nisi.

Nunc euismod sapien sed odio condimentum, et lobortis nunc dignissim. Mauris id finibus quam. Sed finibus ipsum ac tortor convallis, sit amet imperdiet ex volutpat. Vivamus nibh mauris, feugiat ut venenatis quis, blandit consequat dui. Proin libero tellus, dignissim in commodo nec, consectetur id ante. Quisque sodales nisl ac est maximus, in hendrerit massa elementum. In non ultricies mauris, at fermentum justo. Nunc finibus erat eget est consectetur, a ultricies felis fringilla. Curabitur interdum, urna sed commodo pretium, justo mi congue nibh, eget interdum ante sapien ut ex. Fusce rutrum justo ut purus eleifend tincidunt. Aliquam id aliquet lorem, sit amet imperdiet sapien. Nullam ut justo erat. Sed augue arcu, condimentum ac lobortis quis, blandit sit amet est. Vivamus vel tincidunt orci.

Sed molestie sagittis dolor, non rhoncus enim condimentum vitae. Phasellus fringilla sem quis felis dictum tincidunt. Fusce vel enim a leo faucibus lobortis. Quisque accumsan urna at mauris tempus, sit amet suscipit nisl mollis. Suspendisse eu congue tortor. Maecenas rutrum mauris a hendrerit convallis. Praesent pharetra ac magna sit amet pharetra. Phasellus tortor dui, malesuada eget nunc ac, tincidunt mollis eros. Ut cursus, enim a vulputate rhoncus, enim erat sodales neque, at dictum leo nibh eu purus.

Proin facilisis nunc eget est aliquam venenatis. Pellentesque dapibus sem at elit cursus pulvinar. Aliquam magna nibh, consequat non nisl ac, dignissim molestie erat. Phasellus fringilla leo posuere accumsan aliquam. Sed tempor ut odio quis laoreet. Cras nec accumsan nisi, ut bibendum mi. Morbi sit amet malesuada eros, in tincidunt elit. Phasellus eget condimentum enim, sed maximus magna. Donec pretium libero ac purus scelerisque, a elementum est finibus. Phasellus cursus id neque vel pellentesque.

Aliquam erat volutpat. Donec eu justo ullamcorper, placerat risus a, tincidunt nisi. Donec lorem risus, elementum tempor mollis interdum, vulputate vitae libero. In fringilla orci a massa placerat, sed volutpat turpis rhoncus. Duis et feugiat mi, eu cursus urna. Integer iaculis pretium ligula, non hendrerit tortor porta pulvinar. Proin cursus magna sed gravida dapibus. Morbi mauris ipsum, venenatis nec tristique nec, eleifend ac tellus.



Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam volutpat arcu nisl, a varius turpis consequat id. Phasellus eleifend purus id rutrum vestibulum. Fusce ultricies sem at tincidunt interdum. Nullam sit amet leo eros. Ut eget massa sit amet urna tincidunt faucibus in quis ex. Morbi sed nisl vitae tortor vestibulum aliquam at non magna. Cras id congue felis. Suspendisse porttitor sodales erat, eget viverra enim egestas sit amet. Morbi in justo vitae leo aliquet auctor. Donec massa nisi, vestibulum sed ligula ac, egestas fringilla nulla. Etiam lacinia eleifend ipsum eget egestas. Sed lacinia semper massa laoreet malesuada. Sed ac justo nulla. Proin dui nisi, rutrum sed massa finibus, auctor congue nibh. Mauris porttitor, dui a finibus sodales, leo purus feugiat dolor, eget volutpat nisi velit non nulla. Duis vitae ornare nisi.

Nunc euismod sapien sed odio condimentum, et lobortis nunc dignissim. Mauris id finibus quam. Sed finibus ipsum ac tortor convallis, sit amet imperdiet ex volutpat. Vivamus nibh mauris, feugiat ut venenatis quis, blandit consequat dui. Proin libero tellus, dignissim in commodo nec, consectetur id ante. Quisque sodales nisl ac est maximus, in hendrerit massa elementum. In non ultricies mauris, at fermentum justo. Nunc finibus erat eget est consectetur, a ultricies felis fringilla. Curabitur interdum, urna sed commodo pretium, justo mi congue nibh, eget interdum ante sapien ut ex. Fusce rutrum justo ut purus eleifend tincidunt. Aliquam id aliquet lorem, sit amet imperdiet sapien. Nullam ut justo erat. Sed augue arcu, condimentum ac lobortis quis, blandit sit amet est. Vivamus vel tincidunt orci.

Sed molestie sagittis dolor, non rhoncus enim condimentum vitae. Phasellus fringilla sem quis felis dictum tincidunt. Fusce vel enim a leo faucibus lobortis. Quisque accumsan urna at mauris tempus, sit amet suscipit nisl mollis. Suspendisse eu congue tortor. Maecenas rutrum mauris a hendrerit convallis. Praesent pharetra ac magna sit amet pharetra. Phasellus tortor dui, malesuada eget nunc ac, tincidunt mollis eros. Ut cursus, enim a vulputate rhoncus, enim erat sodales neque, at dictum leo nibh eu purus.

Proin facilisis nunc eget est aliquam venenatis. Pellentesque dapibus sem at elit cursus pulvinar. Aliquam magna nibh, consequat non nisl ac, dignissim molestie erat. Phasellus fringilla leo posuere accumsan aliquam. Sed tempor ut odio quis laoreet. Cras nec accumsan nisi, ut bibendum mi. Morbi sit amet malesuada eros, in tincidunt elit. Phasellus eget condimentum enim, sed maximus magna. Donec pretium libero ac purus scelerisque, a elementum est finibus. Phasellus cursus id neque vel pellentesque.

Aliquam erat volutpat. Donec eu justo ullamcorper, placerat risus a, tincidunt nisi. Donec lorem risus, elementum tempor mollis interdum, vulputate vitae libero. In fringilla orci a massa placerat, sed volutpat turpis rhoncus. Duis et feugiat mi, eu cursus urna. Integer iaculis pretium ligula, non hendrerit tortor porta pulvinar. Proin cursus magna sed gravida dapibus. Morbi mauris ipsum, venenatis nec tristique nec, eleifend ac tellus.

     #%d","timestamp":"%s"}' "$i" "$TS")
    REQUEST_BODY=$(jq -n --arg payload "$PAYLOAD" '{
        "properties": {},
        "routing_key": "'"$ROUTING_KEY"'",
        "payload": $payload,
        "payload_encoding": "string"
    }')
    curl -s -u "$RABBITMQ_USER:$RABBITMQ_PASS" \
        -H "Content-Type: application/json" \
        -X POST "$RABBITMQ_URL" \
        -d "$REQUEST_BODY" > /dev/null
}

export -f send_message
export RABBITMQ_USER RABBITMQ_PASS RABBITMQ_URL ROUTING_KEY

# 使用 xargs 并发发送
seq 1 $TOTAL_MESSAGES | xargs -P $MAX_PARALLEL -I {} bash -c 'send_message "$@"' _ {}

echo "完成！总共发送了 $TOTAL_MESSAGES 条消息"


