import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;


public class TestApp2 extends Application {
	Label label;
    TextField field;
    Button button;

	public static void main(String[] args) {
		launch(args);
	}

	/*
	@Override
    public void start(Stage stage) throws Exception {
        label = new Label("This is JavaFX!");
        field = new TextField();
        field.setText("hello");
        field.setPromptText("hello");
        button = new Button("Click");
        BorderPane pane = new BorderPane();
        pane.setTop(label);
        pane.setCenter(field);
        pane.setBottom(button);
        Scene scene = new Scene(pane, 320, 200);
        stage.setScene(scene);
        stage.show();
    }
    */
	
	@Override
	public void start(Stage stage) throws Exception {
        label = new Label("This is JavaFX!");
        field = new TextField();
        button = new Button("Click");
        // アクションイベント処理の組み込み
        button.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent e) {
                String msg = "you typed: " + field.getText();
                label.setText(msg);
            }
        });
        BorderPane pane = new BorderPane();
        pane.setTop(label);
        pane.setCenter(field);
        pane.setBottom(button);
        Scene scene = new Scene(pane, 320, 120);
        stage.setScene(scene);
        stage.show();
    }
}
