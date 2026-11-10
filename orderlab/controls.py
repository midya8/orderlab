"""Original bounded teaching rankings, not real election or preference data."""
def model(n,rows,start=None):return dict(version=1,candidates=n,ballots=[dict(order=o,weight=w)for o,w in rows],start=list(range(n))if start is None else start)
def controls():
 return [dict(id=k,input=p)for k,p in [
 ('strict_local_gap',model(3,[([0,1,2],3),([1,2,0],2),([2,0,1],2)],[1,2,0])),
 ('equal_cycle',model(3,[([0,1,2],1),([1,2,0],1),([2,0,1],1)])),
 ('unanimous',model(4,[([2,0,3,1],4)],[1,3,0,2])),
 ('opposite_ties',model(4,[([0,1,2,3],1),([3,2,1,0],1)])),
 ('one_candidate',model(1,[([0],7)])),
 ('two_candidate_tie',model(2,[([0,1],3),([1,0],3)])),
 ('two_candidate_strict',model(2,[([0,1],4),([1,0],3)],[1,0])),
 ('condorcet_with_tail_cycle',model(4,[([3,0,1,2],3),([3,1,2,0],2),([3,2,0,1],2)],[1,2,0,3])),
 ('duplicate_ballots',model(3,[([0,1,2],1),([0,1,2],2),([1,2,0],2),([2,0,1],2)],[1,2,0])),
 ('six_way_ties',model(6,[([0,1,2,3,4,5],1),([5,4,3,2,1,0],1)])),
 ('five_candidates',model(5,[([0,3,1,4,2],4),([4,2,0,1,3],2),([2,1,3,0,4],3)],[4,3,2,1,0])),
 ('six_candidates',model(6,[([0,2,4,1,3,5],3),([5,3,1,4,2,0],2),([1,2,3,4,5,0],1)],[5,4,3,2,1,0])),
 ('heavy_minority',model(3,[([0,1,2],1000),([2,1,0],999)],[2,1,0])),
 ('descent_moves',model(4,[([0,1,2,3],4),([1,3,2,0],2),([2,0,3,1],1)],[3,2,1,0])),
 ('nonunanimous_acyclic',model(3,[([0,1,2],3),([0,2,1],2),([1,0,2],1)])),
 ('duplicate_order_start',model(3,[([2,1,0],2),([0,2,1],3)],[2,1,0]))]]
