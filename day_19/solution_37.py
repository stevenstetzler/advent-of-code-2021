import numpy as np
import io
import argparse
from day_15.solution_29 import dijkstra

def pairwise_distances(beacons):
    distances = {}
    for i, beacon_1 in enumerate(beacons):
        for j, beacon_2 in enumerate(beacons):
            if j <= i:
                continue
            distance = (np.sum((beacon_1 - beacon_2)**2))**0.5
            # distances.append(np.array(tuple(beacon_1) + tuple(beacon_2) + (distance,)))

            beacon_1_distances = distances.get(tuple(beacon_1), {})
            beacon_1_distances[tuple(beacon_2)] = distance
            distances[tuple(beacon_1)] = beacon_1_distances
            beacon_2_distances = distances.get(tuple(beacon_2), {})
            beacon_2_distances[tuple(beacon_1)] = distance
            distances[tuple(beacon_2)] = beacon_2_distances

    return distances

def associate_distances(distances_1, distances_2):
    matching_points = {x1 : [] for x1 in distances_1.keys()}
    for x1 in distances_1.keys():
        # print(x1)
        for x2, d1 in distances_1[x1].items():
            # print(x1, x2, d1)
            for x3 in distances_2.keys():
                for x4, d2 in distances_2[x3].items():
                    if d1 == d2:
                        # print("matching pair", x1, x2, x3, x4)
                        matching_points[x1].append((x3, x4))
                        matching_points[x2].append((x3, x4))
                        # matching_points[x1].append(x4)
                        # matching_points[x2].append(x3)
                        # matching_points[x2].append(x4)
        # scanner_0_x1, scanner_0_x2, d = scanner_0_pair[0:3], scanner_0_pair[3:6], scanner_0_pair[6]
        # find which pairs in scannner 1 have the same distance
        # matching_pairs = scanner_1_distances[scanner_1_distances[:, 6] == d]
    
    association = {}
    for x1 in matching_points.keys():
        # print(x1, "could be", matching_points[x1])
        # find the point that appears in all matching pairs
        for x2, x3 in matching_points[x1]:
            in_all_pairs_2 = True
            in_all_pairs_3 = True
            for x4, x5 in matching_points[x1]:
                in_all_pairs_2 &= ((np.array(x2) == np.array(x4)).all() or (np.array(x2) == np.array(x5)).all())
                in_all_pairs_3 &= ((np.array(x3) == np.array(x4)).all() or (np.array(x3) == np.array(x5)).all())
            if in_all_pairs_2:
                # print(x1, "is", x2)
                if association.get(x1, None):
                    if not (np.array(x2) == np.array(association[x1])).all():
                        raise Exception(f"{x1} is being assigned {x2} when it is already assigned {association[x1]}")
                association[x1] = x2
            if in_all_pairs_3:
                # print(x1, "is", x3)
                if association.get(x1, None):
                    if not (np.array(x3) == np.array(association[x1])).all():
                        raise Exception(f"{x1} is being assigned {x3} when it is already assigned {association[x1]}")
                association[x1] = x3
            if in_all_pairs_2 and in_all_pairs_3:
                raise Exception(f"{x1} could be either {x2} or {x3}")
    return association
    # for k, v in association.items():
        # print(k, "is", v)
    # print(len(association))

def generate_right_handed_coordinate_systems(verbose=False):
    # permutations of x, y, z: there are 6
    # x, y, z -> x, y, z
    # x, y, z -> z, x, y
    # x, y, z -> y, z, x
    # x, y, z -> x, z, y
    # x, y, z -> y, x, z
    # x, y, z -> z, y, x
    # negations of x, y, z: there are 7
    # x, y, z -> -x, y, z
    # x, y, z -> x, -y, z
    # x, y, z -> x, y, -z
    # x, y, z -> -x, -y, z
    # x, y, z -> -x, y, -z
    # x, y, z -> x, -y, -z
    # x, y, z -> -x, -y, -z
    # rotations about y: (3)
    # x, y, z -> x, y, z
    # x, y, z -> z, y, -x
    # x, y, z -> -x, y, -z
    # x, y, z -> -z, y, x
    # rotations about x: (3)
    # x, y, z -> x, y, z
    # x, y, z -> x, z, -y
    # x, y, z -> x, -y, -z
    # x, y, z -> x, -z, y
    # rotations about z: (3)
    # x, y, z -> x, y, z
    # x, y, z -> y, -x, z
    # x, y, z -> -x, -y, z
    # x, y, z -> -y, x, z

    # XYXYXY =? XXXYYY
    # XY - YX = 
    # X^a * Y^b * Z^c 
    # X^4 = 1, Y^4 = 1, Z^4 = 1
    # XY = -YX
    # a, b, c in [0, 3] --> 4x4x4 = 64 possible words

    # In total, each scanner could be in any of 24 different orientations: 
    # facing positive or negative x, y, or z, and considering any of four
    # directions "up" from that facing.
    # 
    # x, y, z -> x, y, z
    # x, y, z -> x, -y, -z
    # x, y, z -> x, z, -y
    # x, y, z -> x, -z, y
    # 
    # x, y, z -> -x, -y, -z
    # x, y, z -> -x, z, -y
    # x, y, z -> -x, -z, y

    xyz = ["x", "y", "z"]
    sign = ["+", "-"]

    permutations = []
    negations = []

    # generate the 24 permutations and negations of x, y, z that 
    # produce a right-handed coordinate system

    for i in [0, 1, 2]:
        for a in [0, 1]:
            # print(first_letter)
            js = [0, 1, 2]
            js.remove(i)
            # print(i, js)
            for j in js:
                for b in [0, 1]:
                    # print(" " + second_letter)
                    ks = [k for k in js]
                    ks.remove(j)
                    k = ks[0]
                    l = [i, j, k]
                    # an out-of-xyz-order permutation should flip the sign of the first
                    # coordinate to keep it right-handed
                    ordered = False
                    for m in range(0, 3):
                        l1 = l[m:] + l[:m]
                        if all([e1 == e2 for e1, e2 in zip(l1, [0, 1, 2])]):
                            ordered = True
                    
                    xor = lambda _1, _2 : _1 != _2
                    no_flip = xor(a == 1, ordered)
                    flip = not no_flip
                    # flip = (not ordered) == (a == 0)
                    # flip = not ((a == 1) != (ordered))
                    
                    # a = 0 and ordered : no flip     False
                    # a = 1 and ordered : flip        True
                    # a = 0 and not ordered : flip    True
                    # a = 1 and not ordered : no flip False
                    # ordered | a | a == 0 | flip
                    # -----------------------------
                    # True    | 0 | True   | False
                    # True    | 1 | False  | True
                    # False   | 0 | True   | False
                    # False   | 1 | False  | True

                    if flip:
                        c = [0, 1]
                        c.remove(b)
                        c = c[0]
                    else:
                        c = b

                    
                    if verbose:
                        first_letter = f"{sign[a]}{xyz[i]}"
                        second_letter = f"{sign[b]}{xyz[j]}"
                        third_letter = f"{sign[c]}{xyz[k]}"
                        print(first_letter, second_letter, third_letter)
                    
                    permutations.append((i, j, k))
                    negations.append((int(f"{sign[a]}1"), int(f"{sign[b]}1"), int(f"{sign[c]}1")))

    return permutations, negations

def orient(position, permutation, negation):
    oriented = [0 for _ in position]
    for i, (p, n) in enumerate(zip(permutation, negation)):
        oriented[i] = n * position[p]
    return tuple(oriented)

def calculate_offset(shared_beacons, permutations, negations, verbose=False):
    offsets = {}

    for beacon_1, beacon_2 in shared_beacons.items():
        for permutation, negation in zip(permutations, negations):
            # orient the beacon 2 position with a test orientation relative to beacon 1
            beacon_2_oriented = orient(beacon_2, permutation, negation)
            offset = tuple([beacon_1[i] - beacon_2_oriented[i] for i in range(len(beacon_1))])

            if offsets.get(permutation + negation, None):
                offsets[permutation + negation].append(offset)
            else:
                offsets[permutation + negation] = [offset]

    orientation, final_offset = None, None
    i = 0
    for k, v in offsets.items():
        # print(k, v)
        reference = v[0]
        # print(k, v)
        # print([all([coord[i] == reference[i] for i in range(len(coord))]) for coord in v])
        if all([all([coord[i] == reference[i] for i in range(len(coord))]) for coord in v]):
            if verbose:
                print("permutation rule", k[0:3], "and negation rule", k[3:], "works and produces offset", reference)
            orientation, final_offset = k, v[0]
            i += 1

    if i > 1:
        print("  warning: there is more than one orientation that produces valid offsets")

    return orientation, final_offset
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    args, _ = parser.parse_known_args()
    test = args.test
    verbose = args.verbose

    if test:
        infile = "test_input"
    else:
        infile = "input"
    
    with open(infile, "r") as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]

    # calculate_offset(None)
    # return

    scanners = []
    beacons = []
    next = False
    for line in lines:
        if "scanner" in line:
            if len(beacons) > 0:
                next = True
            continue
        if next:
            scanners.append(np.array(beacons))
            beacons = []
            next = False
        if line != "":
            beacons.append(np.array(list(map(int, line.split(",")))))
    if len(beacons) > 0:
        scanners.append(np.array(beacons))

    scanner_0_distances = pairwise_distances(scanners[0])
    scanner_1_distances = pairwise_distances(scanners[1])
    permutations, negations = generate_right_handed_coordinate_systems()

    # find pairs of beacons that have the same distances
    orientations_and_offsets = {}
    for i, scanner_1 in enumerate(scanners):
        for j, scanner_2 in enumerate(scanners):
            if j <= i:
                continue
            association = associate_distances(pairwise_distances(scanner_1), pairwise_distances(scanner_2))
            if len(association) >= 12:
                if verbose:
                    print(f"can associate scanner {i} and {j} with {len(association)} beacons")
                    for k, v in association.items():
                        print(k, "is", v)
                # return
                # try:
                orientation, offset = calculate_offset(association, permutations, negations, verbose=verbose)
                orientations_and_offsets[(i, j)] = (orientation, offset)
                association = associate_distances(pairwise_distances(scanner_2), pairwise_distances(scanner_1))
                orientation, offset = calculate_offset(association, permutations, negations, verbose=verbose)
                orientations_and_offsets[(j, i)] = (orientation, offset)
                
                # except:
                #     pass
            else:
                print(f"associated distances for only {len(association)} beacons for scanner {i} and {j}")
                try:
                    orientation, offset = calculate_offset(association, permutations, negations, verbose=verbose)
                except:
                    pass
    

    offsets_relative_to_0 = {}

    # iteratively fill all offset pairs
    # want to generate a path from 2 to 0 even though it doesn't exist
    # how to find 2 -> 4 -> 1 -> 0?
    # notice that 2 -> 0 doesn't exist
    # is there any path from 2? yes: 2 -> 4
    # is there a path from 4 to 0? if yes: return 2 -> 4 -> 0 else: 
    # is there any path from 4? yes: 4 -> 1
    # is there a path from 1 to 0? if yes: return 2 -> 4 -> 1 -> 0 else: ...

    # all_offsets = {}
    # for (i, j), (orientation, offset) in orientations_and_offsets.items():
    #     all_offsets[(i, j)] = offset
    #     all_offsets[(j, i)] = tuple([-1 * o for o in offset])
    
    # for i in range(1, len(scanners)):
    #     if all_offsets.get((0, i), None) is None:
    #         # try to get from 0 to i
    #         pass

    # for i in range(1, len(scanners)):
    #     for j in range(1, len(scanners)):
    #         if j <= i:
    #             continue
    #         if all_offsets.get((i, j), None):
    #             continue
    #         if orientations_and_offsets.get((i, j), None):
    #             all_offsets[(i, j)] = orientations_and_offsets.get((i, j))[1]
    #             all_offsets[(j, i)] = tuple([-1 * c for c in orientations_and_offsets.get((i, j))[1]])
    #         else:
    #             # search for more pairs
    #             for k in range(1, len(scanners)):
    #                 if orientations_and_offsets.get((i, j), None)

    # find a path from 0 to 2 given the graph
    #   0 1 2 3 4
    # 0   x 
    # 1       x
    # 2
    # 3
    # 4   x x

    for i in range(1, len(scanners)):
        # straightforward: there is a path from i to 0
        if orientations_and_offsets.get((0, i), None):
            orientation, offset = orientations_and_offsets.get((0, i))
            offsets_relative_to_0[i] = offset
    
    for i in range(1, len(scanners)):
        # check if there are other paths to 0
        # e.g. 
        for j in range(1, len(scanners)):
            if j <= i:
                continue
            if orientations_and_offsets.get((i, j), None):
                orientation, offset = orientations_and_offsets.get((i, j))
                if orientations_and_offsets.get((0, i), None):
                    orientation_i_to_0, offset_i_to_0 = orientations_and_offsets.get((0, i))
                    offsets_relative_to_0[j] = tuple([offset[k] + n * offset_i_to_0[k] for k, n in enumerate(orientation_i_to_0[3:])])

                new_offsets = True

    for (i, j), (orientation, offset) in orientations_and_offsets.items():
        print(f"scanner {j} is oriented at {orientation} relative to {i} and offset {offset} in scanner {i}'s frame")
        # if i > 0:
        #     if 

    for i, offset in offsets_relative_to_0.items():
        print(f"scanner {i} is offset {offset} from scanner {0}")


    nodes = set()
    edges = dict()
    weights = dict()
    for (i, j) in orientations_and_offsets.keys():
        nodes.add(i)
        nodes.add(j)
        weights[i] = 1
        weights[j] = 1
        if edges.get(i, None):
            edges[i] += [j]
        else:
            edges[i] = [j]
        if edges.get(j, None):
            edges[j] += [i]
        else:
            edges[j] = [i]
    
    paths = []
    for i in range(1, len(scanners)):
        _, path = dijkstra(0, i, nodes, edges, weights)
        unraveled = [i]
        j = i
        while path.get(j, False):
            unraveled.append(path.get(j))
            j = path.get(j)
        # if verbose:
        print(f"path from 0 to {i}:", unraveled, path)
        paths.append(path)

    for i in range(1, len(scanners)):
        # print(f"finding offset from {i} to 0")
        path = paths[i - 1]
        # resolve the path to calculate offset
        total_offset = (0, 0, 0)
        j = i
        print(j, path.get(j))
        while path.get(j, None) is not None:
            if orientations_and_offsets.get((j, path.get(j)), None):
                # print("getting", j, "to", path.get(j))
                orientation, offset = orientations_and_offsets.get((j, path.get(j)))
                # orientation = tuple([o for o in orientation[:3]] + [-1 * o for o in orientation[3:]])
            else:
                # print("getting", path.get(j), "to", j)
                orientation, offset = orientations_and_offsets.get((path.get(j), j))
            if j < path.get(j):
                total_offset = [total_offset[l] + offset[l] for l, (k, n) in enumerate(zip(orientation[:3], orientation[3:]))]
            j = path.get(j)
            # print(i, "to", j, orientation, offset)
            print(f"offset from {i} to {j} is", total_offset)

        total_offset = tuple(total_offset)
        # print(f"offset from 0 to {i} is", total_offset)

    return 
    # for beacon_1 in scanners[0]:
    #     for beacon_2 in scanners[0]:
    #         distance = (np.sum((beacon_1 - beacon_2)**2))**0.5
    #         if distance == 0:
    #             continue
    #         else:
    #             scanner_0_distances.append((beacon_1, beacon_2, distance))
    
    # print(np.array(scanner_0_distances))
    # print(scanner_1_distances)
    overlapping = []
    for d in scanner_0_distances[:, 6]:
        if np.any(scanner_1_distances[:, 6] == d):
            overlapping.append(
                (
                    scanner_0_distances[scanner_0_distances[:, 6] == d],
                    scanner_1_distances[scanner_1_distances[:, 6] == d],
                )
            )

    association = {}

    for ref, _ in overlapping:
        ref = ref[0, 0:3]
        print(ref)
        others = []
        for i, (beacon_0, beacon_1) in enumerate(overlapping):
            if np.all(beacon_0[0, 0:3] == ref):
                others.append((beacon_1[0, 0:3], beacon_1[0, 3:6]))
                # print(i, beacon_0, beacon_1)
        print("there are", len(others), "others")
        in_all_pairs = []
        for other_1, other_2 in others:
            in_pairs = 0
            for other_3, other_4 in others:
                if np.all(other_1 == other_3) and np.all(other_2 == other_4):
                    continue
                if np.all(other_1 == other_3) or np.all(other_1 == other_4):
                    # print(other_1, "is in pair", other_3, other_4)
                    in_pairs += 1
                # else:
                    # print(other_1, "is not in pair", other_3, other_4)
            if in_pairs == len(others) - 1:
                # print(other_1, "is in all pairs")
                in_all_pairs.append(other_1)
        
        if len(in_all_pairs) > 0:
            all_equal = True
            for x1 in in_all_pairs:
                for x2 in in_all_pairs:
                    all_equal &= np.all(x1 == x2)
            # print(all_equal)
            if all_equal:
                # print(ref, "is", in_all_pairs[0])
                if association.get(tuple(ref), None) is None:
                    association[tuple(ref)] = in_all_pairs[0]
                else:
                    assert(np.all(association[tuple(ref)] == in_all_pairs[0]))
            else:
                print(ref, "is associated with more than one point")
        else:
            print(ref, "is not in all pairs")

    print(len(association))
    for k, v in association.items():
        print(k, "is", v)
        

    distances = scanner_0_distances[
        (scanner_0_distances[:, 3] == 459) &
        (scanner_0_distances[:, 4] == -707) &
        (scanner_0_distances[:, 5] == 401)
    ]
    for d in distances[:, 6]:
        if np.any(scanner_1_distances[:, 6] == d):
            print(d, scanner_1_distances[scanner_1_distances[:, 6] == d])


    
if __name__ == "__main__":
    main()
