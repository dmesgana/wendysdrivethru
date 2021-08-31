package ttr.model.player;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.PriorityQueue;

import ttr.model.destinationCards.Destination;
import ttr.model.destinationCards.DestinationTicket;
import ttr.model.destinationCards.Route;
import ttr.model.destinationCards.Routes;
import ttr.model.trainCards.TrainCard;
import ttr.model.trainCards.TrainCardColor;

class claimHell implements Comparable<claimHell>{
	public Route route;
	public int cost;
	
	public claimHell(Route var, int cost){
		this.route = var;
		this.cost = cost;
	}

	@Override
	public int compareTo(claimHell c1) {
		if (this.cost > c1.cost) return 1;
		else if (this.cost < c1.cost) return -1;
		return 0;
	}
}

public class MyPlayer extends Player{
    
    public MyPlayer(String name) {
        super(name);
    }
    public MyPlayer() {
        super("Da One");
    }

    @Override
    public void makeMove() {
    	//pick up new destination ticket
    	/*if(super.getDestinationTickets().size() == 2 && super.getNumTrainPieces() == 45){
    		super.drawDestinationTickets();
    		return;
    	}*/
    	if(super.getDestinationTickets().size() <= 1 && super.getNumTrainPieces() > 35){
    		super.drawDestinationTickets(); 
    		return;
    	}
    	
    	//if num destination tickets != 0 
    	if(super.getDestinationTickets().size() > 0) {
	        DestinationTicket ticket = nextTicket();
	        Destination s = ticket.getFrom();
	        Destination d = ticket.getTo();
	        ArrayList<Destination> path = NeighborHeuristic(s, d);
	        
	        if(path == null){super.removeDestinationTicket(ticket);}
	        
	        //lay rail
	        Route leastDistance = new Route(s, d, 6, TrainCardColor.blue);
	        
	        TrainCardColor needColor = layRail(path, leastDistance);
	        if(needColor == null)return;
	        
	        //draw cards
	        if(grabColor(TrainCardColor.rainbow)){return;}
	        else if(grabColor(needColor)){return;}
	        else{super.drawTrainCard(0); return;}
    	}
    	//then have list of shortest rainbow or color routes (rainbow being more of a priority)
    	else {
    		PriorityQueue<claimHell> whichToClaim = new PriorityQueue<claimHell>();
    		ArrayList<Route> claimAndy = Routes.getInstance().getAllRoutes();
    		for(Route mount : claimAndy){
    			if(mount.getOwner() == null){
	    			int rainbowWeight = 0;
	    			//cost should also depend on the amount of cards in my hand rn
	    			if(mount.getColor() == TrainCardColor.rainbow) rainbowWeight = mount.getCost()/2;
	    			int cost = mount.getCost() - rainbowWeight;
	    			claimHell inst = new claimHell(mount, cost);
	    			whichToClaim.add(inst);
    			}
    		}
    		Route ld = whichToClaim.poll().route;
    		if(ld.getColor() == TrainCardColor.rainbow){
            	for(TrainCardColor color : TrainCardColor.values()){
            		if(super.getNumTrainCardsByColor(color) >= ld.getCost()){
            			claimRoute(ld, color);
            			return;
            		}
            	}
            }
    		//lay rail
            if(ld.getCost() <= super.getNumTrainCardsByColor(ld.getColor())+super.getNumTrainCardsByColor(TrainCardColor.rainbow)) {
            	if(ld.getColor() == TrainCardColor.rainbow){
	            	for(TrainCardColor col : TrainCardColor.values()){
		            	if(ld.getColor() == TrainCardColor.rainbow) continue;
		            	if(super.getNumTrainCardsByColor(col) == getMostCards()) {
		            		claimRoute(ld, col);
		            		return;
		            	}
	                }
            	}
            	else{
	            	claimRoute(ld, ld.getColor());
	                return;
            	}
            }
            if(ld.getCost() <= super.getNumTrainCardsByColor(TrainCardColor.rainbow)) {
            	claimRoute(ld, TrainCardColor.rainbow);
                return;
            }
          //draw cards
	        if(grabColor(TrainCardColor.rainbow)){return;}
	        else if(grabColor(ld.getColor())){return;}
	        else{super.drawTrainCard(0); return;}
    	}
    }

    public TrainCardColor layRail(ArrayList<Destination> path, Route leastDistance) {
    	TrainCardColor nextColor = null;
    	Route ld = leastDistance;
    	ArrayList<Route> connection = new ArrayList<Route>();
    	for(Route rail : Routes.getInstance().getRoutes(path.get(0), path.get(1))){
        	if(rail.getCost() < ld.getCost() || rail.getCost() == ld.getCost()){
        		ld = rail;
        	}
        }
    	
    	if(!Routes.getInstance().isRouteClaimed(ld)) connection.add(ld);
    	
    	for(int y=1; y<path.size()-1; y++){
    		for(Route rail : Routes.getInstance().getRoutes(path.get(y), path.get(y+1))){
    			if(ld.getDest1() != path.get(y) || ld.getDest2() != path.get(y)){
    				ld = rail;
    				continue;
    			}
    			int stay = super.getNumTrainCardsByColor(ld.getColor());
        		int change = super.getNumTrainCardsByColor(rail.getColor());
        		if(change > stay) ld = rail;
    		}
    		if(Routes.getInstance().isRouteClaimed(ld)) continue;
    		connection.add(ld);
    	}
    	ld = pickRoute(connection);
    	System.out.println(ld);
        nextColor = ld.getColor();
        
        if(ld.getColor() == TrainCardColor.rainbow){
        	for(TrainCardColor color : TrainCardColor.values()){
        		if(getMostCards() == super.getNumTrainCardsByColor(color)) nextColor = color;
        		if(super.getNumTrainCardsByColor(color) >= ld.getCost()){
        			claimRoute(ld, color);
        			return null;
        		}
        	}
        }
        if(ld.getCost() <= super.getNumTrainCardsByColor(ld.getColor())+super.getNumTrainCardsByColor(TrainCardColor.rainbow)) {
        	if(ld.getColor() == TrainCardColor.rainbow){
            	for(TrainCardColor col : TrainCardColor.values()){
	            	if(ld.getColor() == TrainCardColor.rainbow) continue;
	            	if(super.getNumTrainCardsByColor(col) == getMostCards()) {
	            		claimRoute(ld, col);
	            		return null;
	            	}
                }
        	}
        	else{
            	claimRoute(ld, ld.getColor());
                return null;
        	}
        }
        if(ld.getCost() <= super.getNumTrainCardsByColor(TrainCardColor.rainbow)) {
        	claimRoute(ld, TrainCardColor.rainbow);
            return null;
        }
        return nextColor;
    }

    public boolean grabColor(TrainCardColor color) {
        int i=1;
        for(TrainCard river: super.getFaceUpCards()) {
            if(river.getColor() == color){
                super.drawTrainCard(i);
                return true;
            }
            i++;
        }
        return false;
    }

    public DestinationTicket nextTicket() {
        DestinationTicket minDest = super.getDestinationTickets().get(0);
        for(DestinationTicket ticket: super.getDestinationTickets()) {
            if(ticket.getValue() < minDest.getValue()) {
                minDest = ticket; 
            }
        }
        return minDest;
    }

public ArrayList<Destination> NeighborHeuristic(Destination from, Destination to){
	
	HashMap<Destination, Integer> openList = new HashMap<Destination, Integer>();
	HashMap<Destination, Destination> parentList = new HashMap<Destination, Destination>();
	
	Destination parent = null;
	openList.put(from, 0);
	parentList.put(from, parent);
	
	while(openList.size() > 0){
		Destination next = null;
		int minCost = 100;
		for(Destination key : openList.keySet()){
			if(openList.get(key) < minCost){
				next = key;
				minCost = openList.get(key);
			}
		}
		
		if(next == to) {
			//construct arraylist of path (destination type)
			ArrayList<Destination> path = new ArrayList<Destination>();
			Destination back = next;
			System.out.println("----------------");
			while(back != null) {
				System.out.println(back);
				path.add(back);
				back = parentList.get(back);
			}
			System.out.println("----------------");
			return path;
		}
		
		parent = next;
		
		for(Destination neighbor : Routes.getInstance().getNeighbors(next)){
			
			ArrayList<Route> routesToNeighbor = Routes.getInstance().getRoutes(next, neighbor);
			for(Route test : routesToNeighbor){
				Player owner = test.getOwner();
				if(owner == null || owner == this){
					int rainbowWeight = 0;
					if(test.getColor() == TrainCardColor.rainbow){
						rainbowWeight = test.getCost()/2;
					}
					int newCost = 0;
					if(owner == this) newCost = openList.get(next);
					else newCost = openList.get(next) + test.getCost() - rainbowWeight;
					if(parentList.containsKey(neighbor)) {
						if(openList.get(neighbor) == null) continue;
						if(newCost < openList.get(neighbor)){
							openList.put(neighbor, newCost);
							parentList.put(neighbor, parent);
						}
						continue;
					}
					if(openList.containsKey(neighbor)){	
						if(newCost < openList.get(neighbor)){
							openList.put(neighbor, newCost);
							parentList.put(neighbor, parent);
						}
					}
					else{
						openList.put(neighbor, newCost);
						parentList.put(neighbor, parent);
					}
				}
				else{
					break;
				}
			}
		}
		openList.remove(next);
	}
	
	return null;
}

public Route pickRoute(ArrayList<Route> concon){
	Route result = null;
	int value = 0;
	for(Route journey : concon){
		value = super.getNumTrainCardsByColor(journey.getColor());
		if(journey.getColor() == TrainCardColor.rainbow) value = getMostCards();
		
		if(journey.getCost() <= value) return journey;
		if(result == null) result = journey;
		
		else if(value > super.getNumTrainCardsByColor(result.getColor())){
			result = journey;
		}
	}
	return result;
}

public int getMostCards(){
	int result = 0;
	for(TrainCardColor color : TrainCardColor.values()){
		if(super.getNumTrainCardsByColor(color) > result){
			result = super.getNumTrainCardsByColor(color);
		}
	}	
	return result;
}

}
