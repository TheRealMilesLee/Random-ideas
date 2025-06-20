#!/usr/bin/env python3
"""
矩阵乘法性能测试报告生成器
用法: python3 report_generator.py [输出文件]
"""

import datetime
import json
import platform
import re
import subprocess
import sys


def get_system_info():
  """获取系统信息"""
  info = {
      'timestamp': datetime.datetime.now().isoformat(),
      'platform': platform.platform(),
      'processor': platform.processor(),
      'architecture': platform.architecture(),
      'python_version': platform.python_version(),
      'cpu_count': None
  }

  # 获取 CPU 核心数
  try:
    import os
    info['cpu_count'] = os.cpu_count()
  except:
    pass

  return info


def run_benchmark(program_path, args):
  """运行基准测试并解析输出"""
  try:
    cmd = [program_path] + args
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode != 0:
      return None, f"程序执行失败: {result.stderr}"

    return parse_output(result.stdout), None
  except subprocess.TimeoutExpired:
    return None, "程序执行超时"
  except Exception as e:
    return None, f"执行错误: {str(e)}"


def parse_output(output):
  """解析程序输出"""
  data = {}

  # 提取关键信息
  patterns = {
      'matrix_size': r'矩阵大小: (\d+)x(\d+)',
      'block_size': r'块大小: (\d+)',
      'thread_count': r'线程数: (\d+)',
      'iterations': r'迭代次数: (\d+)',
      'memory_usage': r'内存使用量约: ([\d.]+) MB',
      'single_thread_time': r'单线程平均时间: ([\d.]+) 秒',
      'multi_thread_time': r'多线程平均时间: ([\d.]+) 秒',
      'speedup': r'加速比: ([\d.]+)x',
      'efficiency': r'效率: ([\d.]+)%',
      'single_gflops': r'单线程性能: ([\d.]+) GFLOPS',
      'multi_gflops': r'多线程性能: ([\d.]+) GFLOPS'
  }

  for key, pattern in patterns.items():
    match = re.search(pattern, output)
    if match:
      if key == 'matrix_size':
        data[key] = int(match.group(1))
      elif key in ['block_size', 'thread_count', 'iterations']:
        data[key] = int(match.group(1))
      else:
        data[key] = float(match.group(1))

  data['raw_output'] = output
  return data


def generate_html_report(results, output_file):
  """生成 HTML 报告"""
  html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>矩阵乘法性能测试报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1, h2 {{ color: #333; }}
        .system-info {{ background: #e3f2fd; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .test-result {{ background: #f3e5f5; padding: 15px; border-radius: 5px; margin-bottom: 15px; }}
        .metric {{ display: inline-block; margin: 5px 10px; padding: 5px 10px; background: #fff; border-radius: 3px; border-left: 4px solid #2196f3; }}
        .performance {{ color: #4caf50; font-weight: bold; }}
        .warning {{ color: #ff9800; }}
        .error {{ color: #f44336; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f2f2f2; }}
        .chart {{ margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>矩阵乘法性能测试报告</h1>

        <div class="system-info">
            <h2>系统信息</h2>
            <div class="metric">时间: {timestamp}</div>
            <div class="metric">平台: {platform}</div>
            <div class="metric">处理器: {processor}</div>
            <div class="metric">CPU 核心数: {cpu_count}</div>
        </div>

        <h2>测试结果</h2>
        {test_results}

        <h2>性能总结</h2>
        <table>
            <tr><th>矩阵大小</th><th>单线程 (GFLOPS)</th><th>多线程 (GFLOPS)</th><th>加速比</th><th>效率</th></tr>
            {summary_table}
        </table>

        <div class="test-result">
            <h3>性能分析</h3>
            <p>{analysis}</p>
        </div>
    </div>
</body>
</html>
"""

  system_info = results['system_info']
  test_results_html = ""
  summary_rows = ""

  for i, result in enumerate(results['benchmarks']):
    if 'error' in result:
      test_results_html += f"""
            <div class="test-result error">
                <h3>测试 {i+1} - 错误</h3>
                <p>{result['error']}</p>
            </div>
            """
      continue

    data = result['data']
    test_results_html += f"""
        <div class="test-result">
            <h3>测试 {i+1} - {data.get('matrix_size', 'N/A')}x{data.get('matrix_size', 'N/A')}</h3>
            <div class="metric">块大小: {data.get('block_size', 'N/A')}</div>
            <div class="metric">线程数: {data.get('thread_count', 'N/A')}</div>
            <div class="metric">迭代次数: {data.get('iterations', 'N/A')}</div>
            <div class="metric">内存使用: {data.get('memory_usage', 'N/A')} MB</div>
            <br>
            <div class="metric performance">单线程: {data.get('single_gflops', 'N/A')} GFLOPS</div>
            <div class="metric performance">多线程: {data.get('multi_gflops', 'N/A')} GFLOPS</div>
            <div class="metric">加速比: {data.get('speedup', 'N/A')}x</div>
            <div class="metric">效率: {data.get('efficiency', 'N/A')}%</div>
        </div>
        """

    summary_rows += f"""
        <tr>
            <td>{data.get('matrix_size', 'N/A')}</td>
            <td>{data.get('single_gflops', 'N/A')}</td>
            <td>{data.get('multi_gflops', 'N/A')}</td>
            <td>{data.get('speedup', 'N/A')}</td>
            <td>{data.get('efficiency', 'N/A')}%</td>
        </tr>
        """

  # 简单的性能分析
  analysis = "性能测试完成。建议查看加速比和效率指标来评估多线程性能提升效果。"

  html_content = html_template.format(
      timestamp=system_info.get('timestamp', 'N/A'),
      platform=system_info.get('platform', 'N/A'),
      processor=system_info.get('processor', 'N/A'),
      cpu_count=system_info.get('cpu_count', 'N/A'),
      test_results=test_results_html,
      summary_table=summary_rows,
      analysis=analysis)

  with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)


def main():
  output_file = sys.argv[1] if len(
      sys.argv) > 1 else 'performance_report.html'

  # 查找程序可执行文件
  program_candidates = [
      './program_macos', './program_linux', './program.exe', './program'
  ]
  program_path = None

  for candidate in program_candidates:
    try:
      result = subprocess.run([candidate, '--help'],
                              capture_output=True,
                              timeout=5)
      if result.returncode == 0:
        program_path = candidate
        break
    except:
      continue

  if not program_path:
    print("错误: 未找到程序可执行文件")
    sys.exit(1)

  print(f"使用程序: {program_path}")
  print("正在运行性能测试...")

  # 测试配置
  test_configs = [['-s', '512', '-i', '3'], ['-s', '1024', '-i', '3'],
                  ['-s', '2048', '-i', '1']]

  results = {'system_info': get_system_info(), 'benchmarks': []}

  for i, config in enumerate(test_configs):
    print(f"运行测试 {i+1}/{len(test_configs)}: {' '.join(config)}")
    data, error = run_benchmark(program_path, config)

    if error:
      results['benchmarks'].append({'error': error})
    else:
      results['benchmarks'].append({'data': data, 'config': config})

  print(f"生成报告: {output_file}")
  generate_html_report(results, output_file)
  print("报告生成完成！")


if __name__ == '__main__':
  main()
  main()
