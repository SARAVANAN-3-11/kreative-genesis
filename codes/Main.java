import java.util.*;

public class Main {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        if(!sc.hasNextInt()){
            System.out.println("No input provided");
            return;
        }

        int n = sc.nextInt();
        int[] arr = new int[n];

        for(int i=0;i<n;i++){
            if(sc.hasNextInt())
                arr[i] = sc.nextInt();
        }

        int target = sc.nextInt();

        for(int i=0;i<n;i++){
            if(arr[i]==target){
                System.out.println(i);
                return;
            }
        }

        System.out.println("Not Found");
    }
}
