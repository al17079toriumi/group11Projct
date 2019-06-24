package reportGeneratorApp;
import java.io.IOException;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class Main extends Application {
	public static Stage stage;
	Scene w0 = null;
	Scene w3 = null;
	Scene w4 = null;

	public static void main(String[] args) {
		launch(args);
	}

	@Override
	public void start(Stage stage){
		Main.stage = stage;
	    changeView("w0.fxml");

	    stage.setTitle("レポート提出支援システム");
	    stage.setHeight(650);
	    stage.setWidth(1000);
	    stage.setMinHeight(630);
	    stage.setMinWidth(745);
        stage.show();
}

	public void changeView(String fxml) {
        try {
            stage.setScene(new Scene(FXMLLoader.load(getClass().getResource(fxml))));
        } catch (IOException e) {
        	e.printStackTrace();
        }
    }
}
