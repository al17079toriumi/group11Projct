import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;

public class TestApp4 extends Application {

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage stage)throws Exception {
            Parent root = (BorderPane)FXMLLoader.load(getClass().getResource("test.fxml"));
            Scene scene = new Scene(root);
            stage.setScene(scene);
            stage.show();
    }
}