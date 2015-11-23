import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Scanner;

public class p3 {
	public static void main(String[] args) throws Exception{
		
		BST theTree = new BST();
		Scanner scan = new Scanner(System.in);
		String scanned;
		
		System.out.println("Reading...");
		scanned = scan.nextLine();//line
		System.out.println("Read from file: " + scanned);
		System.out.println("Splitting... ");
		String[] split = scanned.split("\\s+");//name
		
		
		
//		for(int i = 0; i < split.length; i++){
//			System.out.println(split[i]);
//		}
		
		System.out.println();

		int loc = 0;
		for (int i = 0; i < split.length; i++){
			loc = i;
			if(split[i].equalsIgnoreCase("NULL")){
				break;
			}
			//System.out.println(name[i]);
			theTree.bst_insert(i + 1, split[i]);
			
		}
		
		if (split[loc + 1].equalsIgnoreCase("s")){
			System.out.println("Searching for: " + split[loc + 2]);
			//System.out.println(split[loc + 2] + " exists and has ID: " + theTree.bst_search(split[loc + 2]));
			theTree.bst_search(split[loc + 2]);
			System.out.println("\n\nIn Order Traverse BST\n");
			theTree.inOrderTraverseTree(theTree.root);
			System.out.println("\n\nPre Order Traverse BST\n");
			theTree.preOrderTraverseTree(theTree.root);
			
		} else if (split[loc + 1].equalsIgnoreCase("d")){
			System.out.println("Deleting: " + split[loc + 2]);
			if(theTree.bst_remove(split[loc + 2])){
				System.out.println("Deleted");
			}else{
				System.out.println("Not found");
			}
			System.out.println("\n\nIn Order Traverse BST\n");
			theTree.inOrderTraverseTree(theTree.root);
			System.out.println("\n\nPre Order Traverse BST\n");
			theTree.preOrderTraverseTree(theTree.root);
			
		}
		
		
	
	}
}