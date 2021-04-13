[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ssw1/binder1/HEAD)

# Q-Table Example

## Overview

The environment is grid of variable size (user defined) that contains a number of obstacles.
One agent tries to reach its target starting from the (0, 0) cell.

## Algorithm Outline

The Q-table is intialized (show TBD).

  * For each episode _e_ (from _1_ to _N_)
     - New actions are attempted until either the target or an obstacle areasdf
    reached. The Q-table is updated with new values whenever there is an improved.
       
At the end of all the episodes, the best results are found in the Q-table.

_Note that there is absolutely no guarantee that this algorithm will converge
or that the result will be optimal_.
