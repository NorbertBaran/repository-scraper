abstract class Vehicle {
    abstract void run();
}

class Car extends Vehicle {
    @Override
    void run() {
        System.out.println("Car is running");
    }
}

class Motorcycle extends Vehicle {
    @Override
    void run() {
        System.out.println("Motorcycle is running");
    }
}

public class Main {
    static void run(Vehicle vehicle) {
        System.out.println("start");
        vehicle.run();
        System.out.println("stop");
    }

    public static void main(String[] args) {
        Vehicle vehicle = new Car();
        run(vehicle);
    }
}