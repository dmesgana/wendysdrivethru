package ttr.main;

import ttr.model.player.HumanPlayer;
import ttr.model.player.Player;
import ttr.model.player.MyPlayer;
import ttr.model.player.StupidPlayer;
//import ttr.model.player.Player1;
import ttr.view.scenes.TTRGamePlayScene;

public class TTRMain {

	public static void main(String[] args) {
		
		/* This is the game object required by the engine (essentially just the game window) */
		TicketToRide myGame = new TicketToRide();
		myGame.setFramesPerSecond(60);
		
		/* Initialize two players. This can be any combination of human players or AI players */
		Player player1 = new StupidPlayer();
		Player player2 = new MyPlayer();
		
		/* Setup the scene, and get the game started */
		TTRGamePlayScene scene = new TTRGamePlayScene("Ticket To Ride", "woodBacking.jpg", myGame, player1, player2);
		myGame.setCurrentScene(scene);
		player1.setScene(scene);
		player2.setScene(scene);
		myGame.start();
		scene.playGame();
	}
}




