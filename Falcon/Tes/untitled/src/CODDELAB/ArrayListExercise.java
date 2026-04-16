package CODDELAB;

import java.util.ArrayList;

public class ArrayListExercise {

    public static void main(String[] args) {

        // ==================================================================================
        // 1. Definition & Characteristics of ArrayList (ANIME EDITION: JUJUTSU KAISEN)
        // ==================================================================================

        // 1.1 Definition
        // Imagine an ArrayList as Megumi Fushiguro's Shadow. He can store an unlimited
        // number
        // of Cursed Tools and Shikigami inside it!
        // Just like his shadow, an ArrayList expands dynamically as you add more items.

        // Constructors (The Summoning Rituals):
        // 1) ArrayList(): Creates an empty Shadow storage (Energy cost: low).
        // 2) ArrayList(Collection c): Steals someone else's inventory (like Yuta
        // copying techniques).
        // 3) ArrayList(int capacity): Prepares a specific amount of space (Binding
        // Vow).

        // 1.2 Characteristics
        // - Dynamic Sizing: Expands like a Domain Expansion when more space is needed.
        // - Ordered: Maintains the order of weapons/spirits exactly as you put them in.
        // - Index-based Access: You can summon a specific weapon instantly (Speed:
        // Infinite/O(1)).

        // ==================================================================================
        // 1.5. Example Use Cases (MISSION: MANAGE THE TOKYO STUDENT ROSTER)
        // ==================================================================================
        // INSTRUCTIONS: Help Gojo Sensei manage the students! Replace '__________' with
        // the correct code.

        // 1) Declaration of ArrayList
        // TODO: Create a list of Strings named 'jujutsuSorcerers'
        ArrayList<String> jujutsuSorcerers = new __________();

        // 2) add(element)
        // TODO: Add these students to the class: "Itadori", "Fushiguro", "Kugisaki"
        jujutsuSorcerers.add("____");
        jujutsuSorcerers.add("____");
        jujutsuSorcerers.add("____");

        System.out.println("First Years Assembled: " + jujutsuSorcerers);

        // 3) add(index, element)
        // TODO: A transfer student arrives! Add "Okkotsu" at index 0 (He is special
        // grade after all)
        jujutsuSorcerers.add(____, "____");

        System.out.println("After Yuta joins: " + jujutsuSorcerers);

        // 4) get(index)
        // TODO: Gojo wants to check who is at index 2. Get the name.
        String student = jujutsuSorcerers.get(____);
        System.out.println("Student at index 2 is: " + student);

        // 5) set(index, element)
        // TODO: Sukuna takes over Itadori! Replace "Itadori" (find his index first)
        // with "Ryomen Sukuna"
        // Let's assume Itadori is at index 1 now.
        jujutsuSorcerers.set(____, "____");

        System.out.println("Oh no, Itadori switched!: " + jujutsuSorcerers);

        // 6) remove(index)
        // TODO: Someone got injured in Shibuya... Remove the student at index 3.
        jujutsuSorcerers.remove(____);

        System.out.println("After the Shibuya Incident: " + jujutsuSorcerers);

        // 7) size()
        // TODO: How many students are left standing?
        System.out.println("Remaining students: " + jujutsuSorcerers.____());

        // 8) isEmpty()
        // TODO: Is the school empty?
        if (jujutsuSorcerers.____()) {
            System.out.println("No sorcerers left to fight curses...");
        } else {
            System.out.println("The fight continues!");
        }

        // 9) clear()
        // TODO: The Higher Ups ordered the execution of everyone. Clear the list.
        jujutsuSorcerers.____();

        System.out.println("Post-Culling Game Status: " + jujutsuSorcerers);
    }
}
