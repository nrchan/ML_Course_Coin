class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        pass

    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |    |
        |  1 |  2 |  3 |
        |    |  5 |    |
        |  4 |  c |  6 |
        |    |    |    |
        |  7 |  8 |  9 |
        |    |    |    |       
        """
        def dis(num1, num2):
            import math
            return math.sqrt(num1*num1 + num2*num2)

        def check_grid():
            grid = set()
            speed_ahead = 100
            left = 10000
            right = 10000
            middle = 10000
            side = 0
            if self.car_pos[0] <= 65: # left bound
                grid.add(1)
                grid.add(4)
                grid.add(7)
            elif self.car_pos[0] >= 565: # right bound
                grid.add(3)
                grid.add(6)
                grid.add(9)

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if x <= 40 and x >= -40 :    
                        if y > 0 and y < 300:
                            grid.add(2)
                            if y < 200:
                                speed_ahead = car["velocity"]
                                grid.add(5) 
                        elif y < 0 and y > -200:
                            grid.add(8)
                    if x > -100 and x < -40 :
                        if y > 80 and y < 250:
                            grid.add(3)
                        elif y < -80 and y > -200:
                            grid.add(9)
                        elif y < 80 and y > -80:
                            grid.add(6)
                    if x < 100 and x > 40:
                        if y > 80 and y < 250:
                            grid.add(1)
                        elif y < -80 and y > -200:
                            grid.add(7)
                        elif y < 80 and y > -80:
                            grid.add(4)

            for coin in scene_info["coins"]:
                if coin[0] < self.car_pos[0] - 20 and coin[1] < self.car_pos[1]:
                    left = min(left, dis(self.car_pos[0] - coin[0], self.car_pos[1] - coin[1]))
                if coin[0] > self.car_pos[0] + 20 and coin[1] < self.car_pos[1]:
                    right = min(right, dis(self.car_pos[0] - coin[0], self.car_pos[1] - coin[1]))
                if coin[0] > self.car_pos[0] - 20 and coin[0] < self.car_pos[0] + 20 and coin[1] < self.car_pos[1]:
                    middle = min(middle, dis(self.car_pos[0] - coin[0], self.car_pos[1] - coin[1]))

            if middle <= left and middle <= right:
                side = 0
            elif left <= right and left <= middle:
                side = -1
            elif right <= left and right <= middle:
                side = 1
            else:
                side = 0
            return move(grid= grid, speed_ahead = speed_ahead, side = side)
            
        def move(grid, speed_ahead, side):
            # if self.player_no == 0:
            #     print(grid)
            if len(grid) == 0:
                if side == -1:
                    return ["SPEED", "MOVE_LEFT"]
                elif side == 1:
                    return ["SPEED", "MOVE_RIGHT"]
                else:
                    if self.car_pos[0] > self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0] < self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_RIGHT"]
                    else :return ["SPEED"]
            else:
                if (2 not in grid): # Check forward
                    if side == -1 and 4 not in grid and 1 not in grid:
                        return ["SPEED", "MOVE_LEFT"]
                    elif side == 1 and 6 not in grid and 3 not in grid:
                        return ["SPEED", "MOVE_RIGHT"]
                    else:
                        # Back to lane center
                        if self.car_pos[0] > self.lanes[self.car_lane]:
                            return ["SPEED", "MOVE_LEFT"]
                        elif self.car_pos[0] < self.lanes[self.car_lane]:
                            return ["SPEED", "MOVE_RIGHT"]
                        else :return ["SPEED"]
                else:
                    if (5 in grid): # NEED to BRAKE
                        if (4 not in grid) and (7 not in grid): # turn left 
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        elif (6 not in grid) and (9 not in grid): # turn right
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                        else : 
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                return ["BRAKE"]
                    if (self.car_pos[0] < 60 ):
                        return ["SPEED", "MOVE_RIGHT"]
                    if side == -1 and 4 not in grid and 1 not in grid:
                        return ["SPEED", "MOVE_LEFT"]
                    if side == 1 and 6 not in grid and 3 not in grid:
                        return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid) and (7 not in grid) and side == -1: # turn left 
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and (9 not in grid) and side == 1: # turn right
                        return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                        return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid) and side == -1: # turn left 
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and side == 1: # turn right
                        return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid): # turn left 
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid): # turn right
                        return ["SPEED", "MOVE_RIGHT"]
                    if (4 not in grid) and (7 not in grid) and side == -1: # turn left 
                        return ["MOVE_LEFT"]    
                    if (6 not in grid) and (9 not in grid) and side == 1: # turn right
                        return ["MOVE_RIGHT"]
                    if (4 not in grid) and (7 not in grid): # turn left 
                        return ["MOVE_LEFT"]    
                    if (6 not in grid) and (9 not in grid): # turn right
                        return ["MOVE_RIGHT"]
                                
                    
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass