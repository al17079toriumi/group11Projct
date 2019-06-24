package reportGeneratorApp;
import java.io.File;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonType;
import javafx.scene.control.Label;
import javafx.scene.control.ScrollPane;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.input.DragEvent;
import javafx.scene.input.Dragboard;
import javafx.scene.input.TransferMode;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.Priority;
import javafx.stage.FileChooser;

public class GenerateController {
	private int gridCount;
	static List<String> pathList;
	List<TextField> kadaiNumList;
	List<TextField> claList;
	List<Button> removeButtonList;
	static List<String> reportTextList;
	GridPane grid;

    @FXML Button w3ModoruBtn;
    @FXML Button w3SeiseiBtn;
    @FXML Button w3SentakuBtn;
    @FXML GridPane uploadGrid = new GridPane();
    @FXML ScrollPane uploadSp = new ScrollPane();
    @FXML AnchorPane uploadAp = new AnchorPane();

    @FXML
    public void initialize() {
		gridCount = 1;
		pathList = new ArrayList<String>();
		kadaiNumList = new ArrayList<TextField>();
		claList = new ArrayList<TextField>();
		removeButtonList = new ArrayList<Button>();
		reportTextList = new ArrayList<String>();
    }

	@FXML
    public void backFromW3ToW0(ActionEvent e) {
		if(!(pathList.size() == 0)) {
			Alert backAlert = new Alert(AlertType.CONFIRMATION);
			backAlert.setTitle("ナビゲーションの確認");
			backAlert.setHeaderText("このページを離れると入力したデータが削除されます。");
			backAlert.setContentText("このページから移動してもよろしいですか？");

			Optional<ButtonType> result = backAlert.showAndWait();
			if (result.get() == ButtonType.OK){
		        new Main().changeView("w0.fxml");
			}
		}else {
	        new Main().changeView("w0.fxml");
		}
    }

    public void displayInputForm(String filePath) {

		grid = new GridPane();
		grid.setHgap(10);
		grid.setVgap(10);
		grid.setPadding(new Insets(10, 10, 10, 10));

		Label pathLabel = new Label(filePath);
		pathLabel.setPrefWidth(700);
		grid.add(pathLabel, 0, 0, 5, 1);

		Label label1 = new Label("課題番号");
		label1.setAlignment(Pos.valueOf("CENTER_RIGHT"));
		label1.setPrefWidth(70);
		grid.add(label1, 0, 1);

		TextField kadaiNum = new TextField();
		kadaiNum.setPrefWidth(85);
		kadaiNum.setPromptText("例）3");
		kadaiNumList.add(kadaiNum);
		grid.add(kadaiNum, 1, 1);

		Label label2 = new Label("コマンドライン引数");
		label2.setAlignment(Pos.valueOf("CENTER_RIGHT"));
		label2.setPrefWidth(150);
		grid.add(label2, 2, 1);

		TextField cla = new TextField();
		cla.setPrefWidth(265);
		cla.setPromptText("例）aaa bbb");
		claList.add(cla);
		grid.add(cla, 3, 1);

		Button removeButton = new Button("取消");
		removeButtonList.add(removeButton);
		grid.add(removeButton, 4, 1);
		removeButton.setOnAction(removeHandler);

	    uploadGrid.add(grid, 0, gridCount);
		uploadAp.setPrefHeight(uploadGrid.getHeight()+90);
	    gridCount += 1;
    }
    final EventHandler<ActionEvent> removeHandler = new EventHandler<ActionEvent>(){
        @Override
        public void handle(final ActionEvent event) {
        	int index = removeButtonList.indexOf(event.getSource());
        	deleteRow(uploadGrid, index+1);
        	removeButtonList.remove(index);
        	pathList.remove(index);
        	kadaiNumList.remove(index);
        	claList.remove(index);
        	gridCount -= 1;
        	uploadAp.setPrefHeight(uploadGrid.getHeight()-58);
        }
    };
    static void deleteRow(GridPane grid, final int row) {
        Set<Node> deleteNodes = new HashSet<>();
        for (Node child : grid.getChildren()) {
            // get index from child
            Integer rowIndex = GridPane.getRowIndex(child);
            // handle null values for index=0
            int r = rowIndex == null ? 0 : rowIndex;
            if (r > row) {
                // decrement rows for rows after the deleted row
                GridPane.setRowIndex(child, r-1);
            } else if (r == row) {
                // collect matching rows for deletion
                deleteNodes.add(child);
            }
        }
        // remove nodes from row
        grid.getChildren().removeAll(deleteNodes);
    }

	@FXML
	  public void fileOpenAction(ActionEvent e) {
	    FileChooser fc = new FileChooser();
	    fc.setTitle("選択");
	    fc.getExtensionFilters().addAll(new FileChooser.ExtensionFilter("C file", "*.c"));
	    fc.setInitialDirectory(new File(System.getProperty("user.home")));
	    File file = fc.showOpenDialog(null);
	    displayInputForm(file.getPath());
	    if(file != null) {
	    	pathList.add(file.getPath());
	    }
	 }

	@FXML
	  public void generateReportAction(ActionEvent e) {
		boolean isContainedNull = false;
		boolean isDuplicate = false;
		boolean cancel = false;
		boolean alrtClear = false;
		String reportText = "";
		String compileText = "";
		boolean compileClear = true;

		for(int i=0;i<kadaiNumList.size();i++) {
			if(kadaiNumList.get(i).getText().equals("")) {
				isContainedNull = true;
				break;
			}
		}
		Set<String> checkHash = new HashSet<String>();
		for(int i=0;i<kadaiNumList.size();i++) {
			if(checkHash.contains(kadaiNumList.get(i).getText()) && !(kadaiNumList.get(i).getText().equals(""))) {
				isDuplicate = true;
				break;
			} else {
				checkHash.add(kadaiNumList.get(i).getText());
			}
		}

		if(pathList.size() == 0) {
			Alert notInputAlrt = new Alert(AlertType.WARNING);
			notInputAlrt.setTitle("警告");
			notInputAlrt.setHeaderText(null);
			notInputAlrt.setContentText("Cソースファイルが入力されていません。");
			notInputAlrt.showAndWait();
		}else {
			if(isContainedNull) {
				alrtClear = false;
				Alert isContainedNullAlrt = new Alert(AlertType.CONFIRMATION);
				isContainedNullAlrt.setTitle("");
				isContainedNullAlrt.setHeaderText("未入力の課題番号があります。");
				isContainedNullAlrt.setContentText("そのままレポート生成を実行しますか？");

				Optional<ButtonType> result = isContainedNullAlrt.showAndWait();
				if (result.get() == ButtonType.OK){
					alrtClear = true;
				}else {
					cancel = true;
				}
			}else {
				alrtClear = true;
			}
			if(!(cancel)){
				if(isDuplicate){

					alrtClear = false;
					Alert isDuplicateAlrt = new Alert(AlertType.CONFIRMATION);
					isDuplicateAlrt.setTitle("");
					isDuplicateAlrt.setHeaderText("複数のファイルで同一の課題番号が入力されています。");
					isDuplicateAlrt.setContentText("そのままレポート生成を実行しますか？");

					Optional<ButtonType> result = isDuplicateAlrt.showAndWait();
					if (result.get() == ButtonType.OK){
						alrtClear = true;
					}
				}else {
					alrtClear = true;
				}
			}
		}
		if(alrtClear) {
			for(int i=0;i<pathList.size();i++) {
				compileText = OrderCompile.compile(pathList.get(i));
				reportText = GenerateReport.generateReport(pathList.get(i), kadaiNumList.get(i).getText(), claList.get(i).getText());
				if(compileText.equals("")) {
					reportTextList.add(reportText);
				}else if(compileText.equals("Erroer by Application") || reportText.equals("Erroer by Application")) {
					Alert appErrorAlert = new Alert(AlertType.ERROR);
					appErrorAlert.setTitle("エラー");
					appErrorAlert.setHeaderText("予期せぬエラーが発生しました。");
					appErrorAlert.setContentText("処理を中断します。");
					appErrorAlert.showAndWait();
					reportTextList.clear();
					compileClear = false;
					break;
				}else {
					Alert compileErrorAlert = new Alert(AlertType.ERROR);
					compileErrorAlert.setTitle("エラー");
					compileErrorAlert.setHeaderText(null);
					compileErrorAlert.setContentText("課題"+kadaiNumList.get(i).getText()+":"+pathList.get(i)+"においてコンパイルエラーが発生したため処理を中断しました。以下にエラー内容を記します。");

					Label label = new Label("Compile error message:");

					TextArea textArea = new TextArea(compileText);
					textArea.setEditable(false);
					textArea.setWrapText(false);

					textArea.setMaxWidth(Double.MAX_VALUE);
					textArea.setMaxHeight(Double.MAX_VALUE);
					GridPane.setVgrow(textArea, Priority.ALWAYS);
					GridPane.setHgrow(textArea, Priority.ALWAYS);

					GridPane expContent = new GridPane();
					expContent.setMaxWidth(Double.MAX_VALUE);
					expContent.add(label, 0, 0);
					expContent.add(textArea, 0, 1);

					compileErrorAlert.getDialogPane().setExpandableContent(expContent);

					compileErrorAlert.showAndWait();
					reportTextList.clear();
					compileClear = false;
					break;
				}
			}
			if(compileClear) {
				new Main().changeView("w4.fxml");
			}
		}
	}

	@FXML
	private void uploadDragOver(DragEvent event) {
		Dragboard board = event.getDragboard();
		if(board.hasFiles()) {
			event.acceptTransferModes(TransferMode.COPY);
		}
	}

	@FXML
	private void uploadDropped(DragEvent event) {
		Dragboard board = event.getDragboard();
		String regex = "\\.c$";
		Pattern pattern = Pattern.compile(regex);
		if(board.hasFiles()) {
			board.getFiles().stream().forEach((file) -> {
				Matcher m = pattern.matcher(file.getPath());
			    if((file != null) && (m.find())) {
			    	pathList.add(file.getPath());
					displayInputForm(file.getPath());
			    } else {
			    	Alert notCAlrt = new Alert(AlertType.WARNING);
			    	notCAlrt.setTitle("警告");
			    	notCAlrt.setHeaderText("ドロップされたファイルはフォーマットが正しくありません。");
			    	notCAlrt.setContentText("入力するファイルはCソースファイルです。");
			    	notCAlrt.showAndWait();
			    }
			});
			event.setDropCompleted(true);
		} else {
			event.setDropCompleted(false);
		}
	}

	public static List<String> getPathList(){
		return pathList;
	}
	public static List<String> getReportTextList(){
		return reportTextList;
	}
}