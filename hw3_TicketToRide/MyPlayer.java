package ttr.model.player;

public class MyPlayer extends Player{
    
    public MyPlayer(String name) {
        super(name);
    }
    public MyPlayer() {
        super("Da One");
    }

    @Override
    public void makeMove() {
        TrainCardColor needColor = TrainCardColor.rainbow;

        DestinationTicket ticket = nextTicket();
        Destination s = ticket.getFrom();
        Destination d = ticket.getTo();
        ArrayList<Route> paths = Routes.getInstance.getRoutes(s, d);
        
        Route leastDistance = new Route();
        //lay rail

        if(leastDistance.getCost() == super.getNumTrainCardsByColor(leastDistance.getColor())) {
            claimRoute(leastDistance, leastDistance.gettColor());
            return;
        }
        if(leastDistance.getCost() == super.getNumTrainCardsByColor(TrainCardColor.rainbow)) {
            claimRoute(leastDistance, TrainCardColor.rainbow);
            return;
        }

        if(super.getNumTrainCardsByColor(leastDistance.getColor()) > super.getNumTrainCardsByColor(TrainCardColor.rainbow)) {
            needColor = leastDistance.getColor();
        }


        //draw cards
        if(grabColor(needColor)){return;}
        super.drawTrainCard(0);
        return;
        
        //pick up new destination ticket
        super.drawDestinationTickets();
    }

    public int basicHeuristic(Route start, Route end) {
        return Routes.getInstance.shortestPathcost(start, end);
    }

    public boolean grabColor(TrainCardColor color) {
        int i=0;
        for(TrainCard river: super.getFaceUpCards()) {
            if(river.getColor() == color){
                super.drawTrainCard(i);
                return true;
            }
            i = i++;
        }
        return false;
    }

    public DestinationTicket nextTicket() {
        DestinationTicket minDest = new DestinationTicket(super.tickets[0]);
        for(DestinationTicket ticket: super.tickets) {
            if(ticket.getValue() < minDest.getValue() && !super.completed.contains(ticket)) {
                minDest = ticket; 
            }
        }
        return minDest;
    }
}
