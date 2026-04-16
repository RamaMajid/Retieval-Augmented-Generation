package CODDELAB;

public class LinkedListExercise {

    // ==================================================================================
    // 2. Linked List (ANIME EDITION: ONE PIECE LOG POSE)
    // ==================================================================================

    // 2.1 Definition
    // Imagine the Grand Line. You cannot fly straight to the end. You must travel
    // from
    // Island to Island. Use a Log Pose (Pointer) to find the next island.
    // Each Island (Node) contains adventure (Data) and points to the next
    // destination (Next).

    // 2.2 Basic Structure
    // 1) Node: An Island (e.g., Drum Kingdom, Alabasta).
    // 2) Data: The name of the Island or the Villain there.
    // 3) Next: The Log Pose needle pointing to the next island.
    // 6) Tail: The furthest island you have reached so far.

    // ==================================================================================
    // IMPLEMENTATION (MISSION: NAVIGATE THE GRAND LINE)
    // ==================================================================================
    // INSTRUCTIONS: Help Nami navigate! Replace '__________' with the correct code.

    // 1) Node Class (The Island)
    static class Island {
        String name; // Island Name
        Island next; // Log Pose to next island

        public Island(String name) {
            this.name = ____;
            this.next = ____; // Initially points to nothing (sea)
        }
    }

    // Pointers for the journey
    private Island startIsland; // Head (Reverse Mountain)
    private Island lastIsland; // Tail (Current Location)

    // 2.4 Important Operations

    // 1) Chart a new course (Add Island at the end)
    public void addIsland(String name) {
        Island newIsland = new Island(____);

        // If we haven't started key
        if (startIsland == ____) {
            startIsland = ____;
            lastIsland = ____;
        } else {
            // Point the current last island to the new one
            lastIsland.next = ____;
            // Update the last island to be the new one
            lastIsland = ____;
        }
    }

    // 2) Buster Call (Delete an Island by name)
    // Destruction of an island breaks the chain! We must link the previous island
    // to the next one.
    public void busterCall(String keyName) {
        Island current = startIsland;
        Island prev = null;

        // Case 1: If the starting island is the target (Ohara?!)
        if (current != null && current.name.equals(____)) {
            startIsland = current.____; // Move start to the next one
            return;
        }

        // Case 2: Navigate to find the island
        while (current != null && !current.name.equals(____)) {
            prev = current;
            current = current.____;
        }

        // If the island doesn't exist on the map
        if (current == null)
            return;

        // Unlink the destroyed island
        prev.next = current.____;
    }

    // 3) View Logbook (Print all islands)
    public void printLogbook() {
        Island current = startIsland;
        System.out.print("Grand Line Route: ");
        while (current != ____) {
            System.out.print(current.name + " -> ");
            current = current.____;
        }
        System.out.println("Laugh Tale (End)");
    }

    // 4) Check Log Pose (Search for an island)
    public boolean isIslandOnRoute(String keyName) {
        Island current = startIsland;
        while (current != null) {
            if (current.name.equals(____)) {
                return true; // Island found!
            }
            current = current.____;
        }
        return false; // Lost at sea
    }

    // 6) Count Islands
    public int countIslands() {
        int count = 0;
        Island current = startIsland;
        while (current != null) {
            count++;
            current = current.____;
        }
        return count;
    }

    // MAIN METHOD to test the journey
    public static void main(String[] args) {
        LinkedListExercise grandLine = new LinkedListExercise();

        // The Journey Begins
        grandLine.addIsland("Romance Dawn");
        grandLine.addIsland("Skypiea");
        grandLine.addIsland("Water 7");
        grandLine.addIsland("Wano Kuni");

        // Check the map
        grandLine.printLogbook();
        // Expected: Romance Dawn -> Skypiea -> Water 7 -> Wano Kuni -> Laugh Tale

        // Nami checks if we visited Fishman Island
        System.out.println("Visited Fishman Island? " + grandLine.isIslandOnRoute("Fishman Island"));

        // Buster Call on Ohara (or imagine an island gets destroyed)
        System.out.println("Buster Call initiated on Skypiea!");
        grandLine.busterCall("Skypiea");

        grandLine.printLogbook();
        // Expected: Romance Dawn -> Water 7 -> Wano Kuni -> Laugh Tale

        // Count adventures
        System.out.println("Total Islands visited: " + grandLine.countIslands());
    }
}
