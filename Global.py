DIM_SPACE: int = 3
DIM_DOF: int = 3

# -----------------------------------------------------------------------------
def find_pos(data, id) -> int:
  pos: int = -1
  if 0 < id < len(data) - 1:
    if data[id].id == id:
      return id

  for i, d in enumerate(data):
    if id == d.id:
      pos = i
      break

  return pos
# -----------------------------------------------------------------------------
def get_el_nodes(connectivity: list[int], nodes):
  el_nodes = []
  for id in connectivity:
    pos = find_pos(nodes, id)
    if pos > -1:
      el_nodes.append(nodes[pos])
  return el_nodes
# -----------------------------------------------------------------------------
def counting(surfpath: list[tuple[int, int]]) -> dict[tuple[int, int], int]:
    result: dict[tuple[int, int], int] = {}
    for elem_id, face_id in surfpath:
        i = (elem_id, face_id)
        result[i] = result.get(i, 0) + 1
    return result
# -----------------------------------------------------------------------------
def find_repeating_numbers(counts: dict[tuple[int, int], int],repeating_numbers: int) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    for i in counts:
        if counts[i] >= repeating_numbers:
            result.append(i)
    return result
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------