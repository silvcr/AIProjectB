from n_b.a_star import compute_path, axial_distance, blocksMoved

def wallPath(n,player,player_coords,opp_coords):

    """ Function chooses closest tile to one wall and then returns path from given tile to two walls  """

    # Finds tile closest to left OR bottom wall depending on player
    if (player == "b"):
        player_coords = sorted(player_coords)
    elif (player == "r"):
        player_coords = sorted(player_coords , key=lambda k: [k[1], k[0]])

    # Return distance from tile to two walls on each side
    return wall(player_coords[0],n,player, opp_coords, player_coords)

def wall(start_coord,n,player,opp_coords,player_coords):

    """ Finds two closest wall values for given point and returns number of  blocks needed to form chain between them """
    i = 0
    wallOneDist = n+1
    wallTwoDist = n+1

    # Run through wall for given player
    for i in range(n-1):
        if player == "b":

            # Finding two walls close to blue
            if blocksMoved(player_coords,compute_path(n, start_coord, (0,i), opp_coords, axial_distance)) < wallOneDist:
                wallOneDist = blocksMoved(player_coords,compute_path(n, start_coord, (0,i), opp_coords, axial_distance))
            # Checking against right wall
            if blocksMoved(player_coords,compute_path(n, start_coord, (n-1, i), opp_coords, axial_distance)) < wallTwoDist:
                wallTwoDist = blocksMoved(player_coords,compute_path(n, start_coord, (n-1, i), opp_coords, axial_distance))
        # Find two walls close to red
        elif player == "r":

            # Checking bottom wall
            if blocksMoved(player_coords,compute_path(n, start_coord, (i,0), opp_coords, axial_distance)) < wallOneDist:
                wallOneDist = blocksMoved(player_coords,compute_path(n, start_coord, (i,0), opp_coords, axial_distance))
            # Checking top wall
            if blocksMoved(player_coords,compute_path(n, start_coord, (i,n-1), opp_coords, axial_distance)) < wallTwoDist:
                wallTwoDist = blocksMoved(player_coords,compute_path(n, start_coord, (i,n-1), opp_coords, axial_distance))
        i+=1

    #print(f"For player {player} from {start_coord} to {wallOne} is {wallOneDist}")
    #print(f"For player {player} from {start_coord} to {wallTwo} is {wallTwoDist}")

    return wallOneDist + wallTwoDist

def triangle(placedBlocks):
    """ Function counts how many triangles of a colour are in a board """
    triCount = 0
    n = len(placedBlocks)

    for i in range(n):
        for j in range(i+1,n):
            for k in range(j+1,n):
                if (det(placedBlocks[i][0], placedBlocks[i][1],
                        placedBlocks[j][0], placedBlocks[j][1],
                        placedBlocks[k][0], placedBlocks[k][1])):
                    triCount+=1

    return triCount

def det(x1,y1,x2,y2,x3,y3):
    """ Returns determinant of three points """
    return (x1 * (y2-y3) - y2 * (x2-x3) + 1 * (x2*y3 - y2*x3))


def centreBlocks(n,placedBlocks):
    """ Gives how many centre blocks a colour has  """
    blocks = 0

    # if n is odd
    if n % 2 > 0:
        min = int(round(n/2)-1)
        max = int(round(n/2))+2

    # if n is even
    else:
        min = int(n/2)-1
        max = int(n/2)+1

    for tile in placedBlocks:
        if tile[0] in range(min,max) and tile[1] in range(min,max):
            blocks+=1

    return blocks

def winningTeam(n,player,player_coords,opp_coords):
    """Gives final evaluation of winning team """

    score = 0
    if player == "b":
        opponent = "r"
    else:
        opponent = "b"

    # SCORING FOR 3 FORMS OF EVALUATION

    # Find distance player is from winning
    # If player path is shorter than opponent then give score *need to do 0 condition too
    if wallPath(n,player,player_coords,opp_coords) < wallPath(n,opponent,opp_coords,player_coords):
        score+=1
    elif wallPath(n,player,player_coords,opp_coords) > wallPath(n,opponent,opp_coords,player_coords):
       score-=1


    # Calculating amount of triangles : Score a point for having more triangles

    #if triangle(player_coords) > triangle(opp_coords):
    #    score += 1
    #elif triangle(player_coords) < triangle(opp_coords):
    #    score -= 1

    # Calculating centre blocks: Score a point for having more centre blocks

    if centreBlocks(n,player_coords) > centreBlocks(n,opp_coords):
        score += 1
    elif centreBlocks(n,player_coords) < centreBlocks(n,opp_coords):
        score -= 1

    # Score > 0 = player winning
    # Score < 0 = opponent winning

    return score