import java.awt.Point;

import world.Robot;
import world.World;
import world.GUI;


public class MyRobotClass extends Robot{
	
	@Override
	public void travelToDestination() {
		super.pingMap(new Point(1, 2));
	}
	
public static void main(String[] args){
	try{
		World myWorld = new World(args[0], false);
		
		MyRobotClass myRobot = new MyRobotClass();
		myRobot.addToWorld(myWorld);
		
		myRobot.travelToDestination();
	}
	catch(Exception e){
		e.printStackTrace();
	}
}}