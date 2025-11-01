# Flocking Algorithm/Boid's Algorithm
These algorithm help in mimicing the group or flock movement of a group or flocks of birds. 
### Important points for Boid algorithm-
- **The agent**
  : The boid or bird. Need to store it's position (Co-ordinates) and Velocity means speed and direction (in a vector format)
- **Local perception**
  : Equivalent to boids looking at their surrouding and getting the data, data being other boids and their position and velocity
  - **Perception radius**
      : the boid's within the specified perception radius are only considered while making decisions, these boids are referred as "neighbours" to the self.boid.
- **Behavioral rule** (vector math)
  : These are the rules responsible for the flock-like behavior of the agents
  - **Seperation**
      : The rule means that the self.boid should not crash to it's neighbours.
      > if there are neighbours around self.boid, run away little boid.
  - **Alignment**
      :  Go in the same direction.
      >  Average velocity of the rest of the neighbours.
  - **Cohesion**
      :stay near the center of the neighbours.
      > find average of all position, then find velocity vector moving towards that direction
- **FLOW**
  1. find all neighbours.
  2. calculate the three forces.
  3. Combine and apply all the forces to acceleration of the boid
- **Other "things" based on this concept**
  : Tweaking things in this algorithm gets to -
  - **Leader-Follower method:** /leader-follower.py
    : One boid is leader which follow the goal and other boid follow leader and seperation, alignment, and cohesion.
    - **goal-seeking-** rule is introduced to make it happen 
    - **/all_goal_seek.py** is applying the goal-seeking role to all the boids.
  - **Predator-prey model** 
    : the name is your hint
    - **Prey boid-** all standard rules with a new high-priority **Evasion rule** which means steer away from predator boid
    - **Predator boid-** Change cohesion rule to steer towards nearest prey boids  
  - **Vicsek Model** used to understand events like phase transition (Booo Physics). In this model all boids move at same constant speed, moving in each others average direction and add noise 
