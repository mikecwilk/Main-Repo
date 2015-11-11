import java.text.DateFormatSymbols;
import java.util.Calendar;
import java.util.GregorianCalendar;

public class GregorianCalendaar {
	  public static void main(String[] args){
		  
		  GregorianCalendar d = new GregorianCalendar();
		  int today = d.get(Calendar.DAY_OF_MONTH);
		  int month = d.get(Calendar.MONTH);
		  
		  d.set(Calendar.DAY_OF_MONTH, 1);
		  int weekday = d.get(Calendar.MONTH);
		  
		  int firstDayOfWeek = d.getFirstDayOfWeek();
		  int indent = 0;
		  
		  while (weekday !=  firstDayOfWeek){
			  
			  indent++;
			  d.add(Calendar.DAY_OF_MONTH, -1);
			  weekday = d.get(Calendar.DAY_OF_WEEK);
			  
		  }
		  
		  String[] weekdayNames = new DateFormatSymbols().getShortWeekdays();
		  
		  do{
			  System.out.printf("%4s", weekdayNames[weekday]);
			  d.add(Calendar.DAY_OF_MONTH, 1);
			  weekday = d.get(Calendar.DAY_OF_WEEK);
			  
		  }while(weekday != firstDayOfWeek);
		  System.out.println();
		  
		  for (int i = 1; i <= indent; i++){
			  System.out.print("    ");
		  }
		  
		  d.set(Calendar.DAY_OF_MONTH, 1);
		  
		  do{
			//print the day
			  int day = d.get(Calendar.DAY_OF_MONTH);
			  System.out.printf("%3d", day);
			  
			//mark current day with an *
			  if(day == today) System.out.print("*"); 
			  else System.out.print(" ");
				  
			//advance d to the next day
			  d.add(Calendar.DAY_OF_MONTH, 1);
			  weekday = d.get(Calendar.DAY_OF_WEEK);
			  
			//start a new line at the start of the week
			  if (weekday == firstDayOfWeek) System.out.println();
			  
			  
		  }while(d.get(Calendar.MONTH) == month);
		  
		  //print final end of line if necessary
		  if (weekday != firstDayOfWeek) System.out.println();
		
		  
	  }
}
