import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

class MySMClass(sm.SM):
    startState = 'DRIVE'
    def getNextValues(self, state, inp):
        inp = io.SensorInput()

        i0=inp.sonars[0]
        i1=inp.sonars[1]
        i2=inp.sonars[2]
        i3=inp.sonars[3]
        i4=inp.sonars[4]
        i5=inp.sonars[5]
        i6=inp.sonars[6]
        i7=inp.sonars[7]
        
        if self.state=='DRIVE':         # start position
            if i4>0.5 and i5>0.5:       
               return (state, io.Action(fvel = 0.3, rvel = 0))
            else:                      
                if i7>0.35: 
                   return (state, io.Action(fvel = 0.03, rvel = 0.27))
                else:
                   return ('F', io.Action(fvel = 0.03, rvel = 0.27))

        if self.state=='F':             # follow wall
            if 0.30<i7 and i7<0.31:       
                if i4>0.5 and i5>0.5:
                   return ('F', io.Action(fvel = 0.3, rvel = 0))
                elif i5>0.5 and i6>0.4:
                    return ('F', io.Action(fvel = 0.03, rvel = -0.27))
                else:
                    return ('F', io.Action(fvel = 0.03, rvel = 0.27))

            elif i7<0.3:               
                    return ('F', io.Action(fvel = 0.03, rvel = 0.27))
 
            elif i7>0.3 and (i4<0.35 or i5<0.35):
                    return ('F', io.Action(fvel = 0.03, rvel = 0.27))
            else:
                    return ('F', io.Action(fvel = 0.12, rvel = -0.27))

        
mySM = MySMClass()
mySM.name = 'brainSM'


def plotSonar(sonarNum):
    robot.gfx.addDynamicPlotFunction(y=('sonar'+str(sonarNum),
                                        lambda: 
                                        io.SensorInput().sonars[sonarNum]))

# this function is called when the brain is (re)loaded
def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True, # slime trails
                                  sonarMonitor=False) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    print inp.sonars[1], 
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())
