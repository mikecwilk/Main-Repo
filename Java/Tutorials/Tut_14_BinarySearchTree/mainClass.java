import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.FileReader;

public class mainClass {
	public static void main(String[] args) throws Exception{
		
	
		FileReader file = new FileReader("p3.data1");
		BufferedReader reader = new BufferedReader(file);
		
		BST theTree = new BST();
		
		String[] name = null;		
		String line = reader.readLine();
		int count = 0;
		
		while (line != null){
			name = line.split("\\s+");
			line = reader.readLine();

		}
		for (int i = 0; i < name.length; i++){
			if(name[i].equalsIgnoreCase("NULL")){
				break;
			}
			//System.out.println(name[i]);
			theTree.addNode(i + 1, name[i]);
			
		}
		
		theTree.inOrderTraverseTree(theTree.root);
		System.out.println("\n\n");
		theTree.preOrderTraverseTree(theTree.root);
		

	}
}
