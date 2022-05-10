from n_b.a_star import compute_path, axial_distance, blocksMoved

def calcScore(n,player,player_coords,opp_coords):

    """ Main calculation of evaluation
    Will first file tile closest to a wall then find shortest distance from
    such tile to other wall considering other placed blocks """
    wallDist = n + 1

    # Finds tile closest to a wall
    for point in player_coords:
       if wall(point,n,player,opp_coords,player_coords,"dist") < wallDist:
           closestTile = point
           wallDist = wall(point,n,player,opp_coords,player_coords,"dist")

    # Distance tile is from one wall and to the other wall
    blocksLeft = wall(closestTile, n, player, opp_coords, player_coords,
         "distFromOtherWall") + wall(closestTile,n,player,opp_coords,player_coords,"distFromWall")


    # add triangle(n,player_coords) and centreBlocks but need to figure out scoring

    # Returns blocks left to win and how many blocks placed * will have to change scoring
    return blocksLeft



def triangle(n,placedBlocks):
    """ Function counts how many triangles of a colour are in a board """
    print("Triangle counting ")
    for points in placedBlocks:
        print(points)
    return


def centreBlocks(n,placedBlocks):
    """ Gives score on how many centre blocks there are  """
    return



def wall(start_coord,n,player,opp_coords,player_coords,toReturn):

    """ Finds closest non opponent occupied wall and distance from it - not optimised should fix """
    i = 0
    wallOneDist = n+1
    wallTwoDist = n+1
    shortestDist = n + 1

    # Run through wall for given player
    while i in range(n):
        if player == "b":
            # Comparing path lengths between coord and walls: Allocate new close wall when shorter distance
            # found

            # Finding two walls close to blue
            if blocksMoved(player_coords,compute_path(n, start_coord, (0,i), opp_coords, axial_distance)) < wallOneDist:
                wallOneDist = blocksMoved(player_coords,compute_path(n, start_coord, (0,i), opp_coords, axial_distance))
            # Checking against right wall
            if blocksMoved(player_coords,compute_path(n, start_coord, (n, i), opp_coords, axial_distance)) < wallTwoDist:
                wallTwoDist = blocksMoved(player_coords,compute_path(n, start_coord, (n, i), opp_coords, axial_distance))

        # Find two walls close to red
        else:
            # Checking bottom wall
            if blocksMoved(player_coords,compute_path(n, start_coord, (i,0), opp_coords, axial_distance)) < wallOneDist:
                wallOneDist = blocksMoved(player_coords,compute_path(n, start_coord, (i,0), opp_coords, axial_distance))
            # Checking top wall
            if blocksMoved(player_coords,compute_path(n, start_coord, (i,n), opp_coords, axial_distance)) < wallTwoDist:
                wallTwoDist = blocksMoved(player_coords,compute_path(n, start_coord, (i,n), opp_coords, axial_distance))
        i+=1

    # Assign wall values * can remove big chunk, just keeping now
    if wallOneDist < wallTwoDist:
        distFromWall = wallOneDist
        distFromOtherWall = wallTwoDist

    elif wallOneDist > wallTwoDist:
        distFromWall = wallTwoDist
        distFromOtherWall = wallOneDist

    else:
        # Both same distance
        return wallOneDist

    if toReturn == "distFromWall":
        return distFromWall
    elif toReturn == "distFromOtherWall":
        return distFromOtherWall
    else:
        return distFromWall

# Score > 0 indicates opponent winning
# Score < 0 Indicates player winning
# Score = 0 indicates a draw

def winningTeam(n,player,player_coords,opp_coords):
    """Gives final evaluation of winning team """

    if player == "b":
        opponent = "r"
    else:
        opponent = "b"

    # Find distance player is from winning
    playerDist = calcScore(n,player,player_coords,opp_coords)
    # Find distance opponent is from winning
    opponentDist = calcScore(n,opponent,opp_coords,player_coords)

    # Returns difference of how far each player is from winning and returns winning team
    score = playerDist - opponentDist

    # Higher score means opponent winning
    # Lower score means current player winning
    # 0 indicates a tie

    if score > 0:
        print(f"Opponent is winning")
    elif score < 0:
        print("Player winning")
    else:
        print("Draw")

    return score