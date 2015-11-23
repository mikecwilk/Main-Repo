
public class BST {
	
	Node root;
	
	public void bst_insert(int ID, String name){
		
		Node newNode = new Node (ID, name);
		
		
		if(root == null){
			root = newNode;
			newNode.addName(ID, name);
			
		}else{
			Node focusNode = root;
			
			Node parent;
			
			while(true){
				parent = focusNode;
				
				if(name.compareToIgnoreCase(focusNode.original_name) < 0){ 
					focusNode = focusNode.leftChild;
					
					if (focusNode == null){
						parent.leftChild = newNode;
						newNode.addName(ID, name);
						return;
						
					}
				}else if(name.compareToIgnoreCase(focusNode.original_name) > 0) {
					focusNode = focusNode.rightChild;
					
					if(focusNode == null){
						parent.rightChild = newNode;
						newNode.addName(ID, name);
						return;
					}
				}
				
				else if(name.compareToIgnoreCase(focusNode.original_name) == 0) {
					//System.out.println("Names Match!");
					focusNode.addName(ID, name);
					return;
				}
			}
			
			
		}
		
	}
	
	public boolean bst_remove(String name){
		
		Node focusNode = root;
		Node parent = root;
		
		boolean isLeft = true;
		
		while(!(focusNode.original_name.equals(name))){
			
			parent = focusNode;
			
			if (name.compareToIgnoreCase(focusNode.original_name) < 0){ 
				isLeft = true;
				focusNode = focusNode.leftChild;
			}else{
				isLeft = false;
				focusNode = focusNode.rightChild;
			}
			
			if(focusNode == null){
				return false;
			}
			
		}
		
		if(focusNode.leftChild == null && focusNode.rightChild == null){
			
			if(focusNode == root){
				root = null;
			
			} else if (isLeft){
				parent.leftChild = null;
			
			} else {
				parent.rightChild = null;
			
			}
		}
		
		
		else if(focusNode.rightChild == null){
			
			if(focusNode == root){
				root = focusNode.leftChild;
			} else if (isLeft){
				parent.leftChild = focusNode.leftChild;
			} else parent.rightChild = focusNode;
		}
		
		else if(focusNode.leftChild == null){
			
			if(focusNode == root){
				root = focusNode.rightChild;
			}else if(isLeft){
				parent.leftChild = focusNode.rightChild;
				
			}else parent.rightChild = focusNode.leftChild;			
						
		}
		
		else{
			Node replacement = getReplacementNode(focusNode);
			
			if (focusNode == root) root = replacement;
			
			else if(isLeft) parent.leftChild = replacement;
			
			else parent.rightChild = replacement;
			
			replacement.leftChild = focusNode.leftChild;
			
		}
		
		return true;
	}
	
	public Node getReplacementNode(Node replacedNode){
		Node replacementParent = replacedNode;
		Node replacement = replacedNode;
		
		Node focusNode = replacedNode.rightChild;
		
		while (focusNode != null){
			
			replacementParent = replacement;
			replacement = focusNode;
			focusNode = focusNode.leftChild;
		}
		
		if(replacement != replacedNode.rightChild){
			
			replacementParent.leftChild = replacement.rightChild;
			replacement.rightChild = replacedNode.rightChild;
			
		}
		
		return replacement;
		
	}
	
	public void bst_search(String name){

		if (root == null){
			System.out.println(name + " was not found!");
			return;
		}else{
			Node focusNode = root;
			Node parent = root;
			
			while(!(focusNode.original_name.equalsIgnoreCase(name))){
				parent = focusNode;
				System.out.println("traversing path: " + focusNode.original_name);
				
				if (name.compareToIgnoreCase(focusNode.original_name) < 0){
					
					//isLeft = true;
					focusNode = focusNode.leftChild;
				}else{
					//isLeft = false;
					focusNode = focusNode.rightChild;
				}
				
				if(focusNode == null){
					
					System.out.println(name + " was not found!");
					return;
				}
				
				
			
			}
			System.out.println(name + " was found!");
			focusNode.printNames();
			return;
		}
		
	}
	
	public void inOrderTraverseTree(Node focusNode){
		
		if(focusNode != null){
			inOrderTraverseTree(focusNode.leftChild);
			//System.out.println(focusNode);
			focusNode.printNames();
			
			inOrderTraverseTree(focusNode.rightChild);
		}
		
	}
	
	public void preOrderTraverseTree(Node focusNode){
		
		if(focusNode != null){
			
			focusNode.printNames();
			preOrderTraverseTree(focusNode.leftChild);
			preOrderTraverseTree(focusNode.rightChild);
		}
		
	}

}
