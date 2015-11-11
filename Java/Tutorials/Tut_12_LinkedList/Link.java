
public class Link {
	
	public String bookName;
	public int millionsSold;
	
	public Link next;
	
	public Link(String bookName, int millionsSold){
		
		this.bookName = bookName;
		this.millionsSold = millionsSold;
		
	}
	
	public void display(){
		System.out.println(bookName + ": " + millionsSold + ",000,000");
	}
	
	public String toString(){
		return bookName;
	}

	public static void main(String[] args){
		LinkList theLinkedList = new LinkList();
		
		theLinkedList.insertFirstLink("Don Quiote", 500);
		theLinkedList.display();
		System.out.println();
		theLinkedList.insertFirstLink("A Tale of Two Cities", 200);
		theLinkedList.display();
		System.out.println();
		theLinkedList.insertFirstLink("The Lord of the Rings", 150);
		theLinkedList.display();
		System.out.println();
		theLinkedList.insertFirstLink("Harry Potter and the Sorcerers Stone", 100);
		
	
		
		theLinkedList.removeFirst();
		
		theLinkedList.display();
		
//		System.out.println(theLinkedList.find("The Lord of the Rings").bookName + " was found");
		
//		theLinkedList.removeLink("The Lord of the Rings");
		
//		theLinkedList.display();
	}
	
}


class LinkList{
	public Link firstLink;
	
	LinkList(){
		firstLink = null;
		
	}
	
	public boolean isEmpty(){
		return (firstLink == null);
	}
	
	public void insertFirstLink(String bookName, int millionsSold){
		Link newLink = new Link(bookName, millionsSold); 
		newLink.next = firstLink;
		firstLink = newLink;
		
	}
	
	public Link removeFirst(){
		Link linkReference = firstLink;
		
		if(!isEmpty()){
			firstLink = firstLink.next;
		}else{
			System.out.println("Empty Linked List");
		}
		
		return linkReference;
	}
	
	public void display(){
		Link theLink = firstLink;
		
		while(theLink != null){
			theLink.display();
			System.out.println("Next Link: " + theLink.next);
			theLink = theLink.next;
			System.out.println();
		}
	}
	
	public Link find (String bookName){
		Link theLink = firstLink;
		
		if (!isEmpty()){
			while(theLink.bookName != bookName){
				if(theLink.next == null){
					return null;
				}else{
					theLink = theLink.next;
				}
			}
		}else{
			System.out.println("Empty LinkedList");
		}
		
		return theLink;
	}
	
	public Link removeLink(String bookName){
		Link currentLink = firstLink;
		Link previousLink = firstLink;
		
		while(currentLink.bookName != bookName){
			if (currentLink.next == null){
				
			}else{
				previousLink = currentLink;
				currentLink = currentLink.next;
			}
		}
		
		if(currentLink == firstLink){
			firstLink = firstLink.next;
		}else{
			previousLink.next = currentLink.next;
		}
		
		return currentLink;
	}
	
}