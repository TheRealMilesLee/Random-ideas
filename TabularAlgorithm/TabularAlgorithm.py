from collections import deque

# ------------------------
# 数据定义
# ------------------------

# 数据流域 D
D = {0, 1}

# exploded nodes
N = ["1_main", "call_f", "2_main", "3_f", "4_f", "return_f"]
N_p = set(N)
Call_p = {"call_f"}
e_p = "return_f"
N_star = N

# exploded edge set E#: ⟨sp, d1⟩ → ⟨n, d2⟩
E_sharp = {
    (("s_main", 0), ("1_main", 0)),
    (("1_main", 0), ("call_f", 0)),
    (("call_f", 0), ("3_f", 0)),  # call to f
    (("3_f", 0), ("4_f", 1)),  # inside f
    (("4_f", 1), ("return_f", 1)),  # return inside f
    (("return_f", 1), ("2_main", 1)),  # back to main
    (("2_main", 1), ("s_exit", 1)),  # exit point
}

# ------------------------
# 辅助函数
# ------------------------


def calledProc(n):
  return {"call_f": "f"}.get(n, None)


def returnSite(n):
  return {"call_f": "2_main"}.get(n, None)


def callers(n):
  # who called procedure n
  return {"f": {"call_f"}}.get(n, set())


def s_proc_of(c):
  return {"call_f": "main"}.get(c, None)


# ------------------------
# Tabulation 主程序
# ------------------------

PathEdge = set()
WorkList = deque()
SummaryEdge = set()


def propagate(edge):
  if edge not in PathEdge:
    PathEdge.add(edge)
    WorkList.append(edge)


def ForwardTabulateSLRPs():
  global PathEdge, WorkList, SummaryEdge
  PathEdge = {(("s_main", 0), ("s_main", 0))}
  WorkList = deque(PathEdge)
  SummaryEdge = set()

  while WorkList:
    (sp, d1), (n, d2) = WorkList.popleft()

    # Case 1: call node
    if n in Call_p:
      for ((src_n, src_d), (dst_n, dst_d)) in E_sharp:
        if (src_n, src_d) == (n, d2):
          propagate(((calledProc(n), dst_d), (calledProc(n), dst_d)))
      for ((src_n, src_d), (dst_n, dst_d)) in E_sharp.union(SummaryEdge):
        if (src_n, src_d) == (n, d2) and dst_n == returnSite(n):
          propagate(((sp, d1), (dst_n, dst_d)))

    # Case 2: return node
    elif n == e_p:
      for c in callers("f"):  # 当前只考虑 f
        for d4 in D:
          if ((c, d4), (sp, d1)) in E_sharp:
            for ((e_src_n, e_src_d), (e_dst_n, e_dst_d)) in E_sharp:
              if (e_src_n, e_src_d) == (e_p, d2) and e_dst_n == returnSite(c):
                if ((c, d4), (e_dst_n, e_dst_d)) not in SummaryEdge:
                  SummaryEdge.add(((c, d4), (e_dst_n, e_dst_d)))
                for d3 in D:
                  if ((s_proc_of(c), d3), (c, d4)) in PathEdge:
                    propagate(((sp, d1), (e_dst_n, e_dst_d)))

    # Case 3: normal node
    elif n in (N_p - Call_p - {e_p}):
      for ((src_n, src_d), (dst_n, dst_d)) in E_sharp:
        if (src_n, src_d) == (n, d2):
          propagate(((sp, d1), (dst_n, dst_d)))


# ------------------------
# 执行并输出
# ------------------------

ForwardTabulateSLRPs()

print("PathEdge:")
for edge in sorted(PathEdge):
  print(edge)

print("\nSummaryEdge:")
for edge in sorted(SummaryEdge):
  print(edge)
