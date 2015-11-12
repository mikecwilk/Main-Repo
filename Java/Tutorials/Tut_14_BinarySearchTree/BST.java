
public class BST {
	
	Node root;
	
	public void addNode(int key, String name){
		
		Node newNode = new Node (key, name);
		
		if(root == null){
			root = newNode;
			
		}else{
			Node focusNode = root;
			
			Node parent;
			
			while(true){
				parent = focusNode;
				
				if(name.compareToIgnoreCase(focusNode.name) < 0){ 
					focusNode = focusNode.leftChild;
					
					if (focusNode == null){
						parent.leftChild = newNode;
						return;
						
					}
				}else{
					focusNode = focusNode.rightChild;
					
					if(focusNode == null){
						parent.rightChild = newNode;
						return;
					}
				}
			}
			
			
		}
		
	}
	
	public void inOrderTraverseTree(Node focusNode){
		
		if(focusNode != null){
			inOrderTraverseTree(focusNode.leftChild);
			System.out.println(focusNode);
			inOrderTraverseTree(focusNode.rightChild);
		}
		
	}
	
	public void preOrderTraverseTree(Node focusNode){
		
		if(focusNode != null){
			
			System.out.println(focusNode);
			preOrderTraverseTree(focusNode.leftChild);

			preOrderTraverseTree(focusNode.rightChild);
		}
		
	}

}
