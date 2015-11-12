public class DoubleEndedLinkedList{

	Neighbor firstLink;
	Neighbor lastLink;
	
	public void insertInFirstPosition(String homeOwnerName, int houseNumber){
		
		Neighbor theNewLink = new Neighbor(homeOwnerName, houseNumber);
		
		if(isEmpty()){
			lastLink = theNewLink;
		} else{
			firstLink.previous = theNewLink;
		}
		
		theNewLink.next = firstLink;
		firstLink = theNewLink;
		
	}
	
	public void insertInLastPosition(String homeOwnerName, int houseNumber){
		Neighbor theNewLink = new Neighbor(homeOwnerName, houseNumber);
		
		if(isEmpty()){
			
			firstLink = theNewLink;
		
		}else{
		
			lastLink.next = theNewLink;
			theNewLink.previous = lastLink;
			
		}
		
		lastLink = theNewLink;
		
	}
	
	public boolean insertAfterKey(String homeOwnerName, int houseNumber, int key){
		Neighbor theNewLink = new Neighbor(homeOwnerName, houseNumber);
		
		Neighbor currentNeighbor = firstLink;
		
		while(currentNeighbor.houseNumber != key){
			
			currentNeighbor = currentNeighbor.next;
			
			if (currentNeighbor == null){
				return false;
			}
		}
		
		if(currentNeighbor == lastLink){
			theNewLink.next = null;
			lastLink = theNewLink;
		}else{
			
			theNewLink.next = currentNeighbor.next;
			currentNeighbor.next.previous = theNewLink;
			
		}
		
		theNewLink.previous = currentNeighbor;
		currentNeighbor.next = theNewLink;
		return true;
	}
	
	public void insertInOrder(String homeOwnerName, int houseNumber){
		
		Neighbor theNewLink = new Neighbor (homeOwnerName, houseNumber);
		Neighbor previousNeighbor = null;
		Neighbor currentNeighbor = firstLink;
		
		while (currentNeighbor != null && (houseNumber > currentNeighbor.houseNumber)){
			
			previousNeighbor = currentNeighbor;
			currentNeighbor = currentNeighbor.next;
			
		}
		
		if(previousNeighbor == null){
			firstLink = theNewLink;
		}else{
			previousNeighbor.next = theNewLink;
		}
		theNewLink.next = currentNeighbor;
	}
	
	public boolean isEmpty(){
		return(firstLink == null);
	}
	
	public static void main(String[] args){
		DoubleEndedLinkedList theLinkedList = new DoubleEndedLinkedList();
		theLinkedList.insertInOrder("Mike", 10);
		theLinkedList.insertInOrder("John", 12);
		theLinkedList.insertInOrder("Jessie", 8);
		theLinkedList.insertInOrder("Bill", 20);
		theLinkedList.insertInOrder("Matty", 21);
		theLinkedList.insertInOrder("Gracie", 25);
		
		theLinkedList.insertAfterKey("Mike", 23, 21);
		
		theLinkedList.display();
		
		System.out.println("\n");
		
		NeighborIterator neighbors = new NeighborIterator(theLinkedList);
		
		neighbors.currentNeighbor.display();
		
		System.out.println(neighbors.hasNext());
		
		neighbors.next();
		
		neighbors.currentNeighbor.display();
		
		neighbors.remove();
		
		neighbors.currentNeighbor.display();
	}
	
	public void display(){
		Neighbor theLink = firstLink;
		
		while(theLink != null){
			theLink.display();
			System.out.println("Next Link: " + theLink.next);
			theLink = theLink.next;
			System.out.println();
		}
	}
	
}