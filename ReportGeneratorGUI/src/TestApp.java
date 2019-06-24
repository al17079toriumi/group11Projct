
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.FlowPane;
import javafx.stage.Stage;

public class TestApp extends Application {

	public static void main(String[] args) {
		launch(args);
	}

	@Override
    public void start(Stage stage) throws Exception {
		Label label = new Label("Hello World!!");
        //BorderPane pane = new BorderPane();
        //pane.setCenter(label);
		FlowPane pane = new FlowPane();
        pane.getChildren().add(label);
        Scene scene = new Scene(pane, 500, 500);
        stage.setScene(scene);
        stage.show();
    }
}
