import math
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import euler_from_quaternion

# TODO Map
# TODO distList

class PositionEstimator(object):

    # used for lookup
    itemList = ['ball', 'hat']
    # needs to be experimented with
    distList = [1,2,4,7]

    # items is like {'hat': 0, 'ball': 2}
    def __init__(self, items, mapName='', verbose=False):
        self.verbose = verbose
        
        # set up list of items to find
        self.target_items = items
        self.found_items = {'hat': 0, 'ball': 0}
        self.found_positions = []

        # set up subscriber for /amcl_pose to update robot position & heading
        self.robot_position = [0,0]
        self.robot_heading = 0.0
        self.sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.robot_moved_callback)
        
        # set up empty map using mapName parameter


        # if requested, give feedback
        if verbose:
            print('Running in verbose mode')
            print('Set up subscriber and publisher')
            print('Set up empty map')
            print('List of target items:')
            print(self.target_items)
        
    # imgType is 0 for ball, 1 for hat
    # position is 0-15
    # return item name and position
    def place(self, imgType, pos):
        itemType = self.itemList[imgType]
        if self.verbose:
            print('Found an item:', itemType)
        # find relative position of item based on 'position'
        h = pos // 4
        w = pos % 4
        angle = -22.5 + (w * 15)
        dist = self.distList[h]
        if self.verbose:
            print('pos:',pos,', h:',h,', w:',w,', angle:',angle,', dist:', dist)

        # find absolute position based on robotPose
        angle = math.radians(angle) + self.robot_heading
        x = self.robot_position[0] + math.cos(angle) * dist
        y = self.robot_position[1] + math.sin(angle) * dist
        
        # add to internal map
        x, y
        
        # update list of items to find
        self.found_items[itemType] = self.found_items[itemType] + 1
        self.found_positions.append([itemType, (x, y)])
        return itemType, (x, y)

    def get_positions(self):
        return self.found_positions

    # when robot moves
    def robot_moved_callback(self, newPose):
        p = newPose.pose.pose.position
        o = newPose.pose.pose.orientation
        if self.verbose:
            print('Robot moved, updating position')
        self.robot_position = [p.x, p.y]
        (discard1, discard2, self.robot_heading) = euler_from_quaternion([o.x, o.y, o.z, o.w])
        if self.verbose:
            print('New location: (', p.x, ',', p.y,')')
            print('New heading: ', self.robot_heading)

    # after program execution, save map with positions of found items
    def save_map(self, filename='treasure_map'):
        if self.verbose:
            print('Saving map')
        # save map

        if self.verbose:
            print('Map saved at \'' + filename + '\'')
        return self
