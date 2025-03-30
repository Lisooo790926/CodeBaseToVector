package com.example.demo.controller;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class UserController {

    /**
     * Get user by ID
     * @param id user identifier
     * @return user information
     */
    @GetMapping("/{id}")
    public String getUserById(@PathVariable Long id) {
        return "User " + id;
    }

    /**
     * Create new user
     * @param userData user information
     * @return created user
     */
    @PostMapping
    public String createUser(@RequestBody String userData) {
        return "Created user: " + userData;
    }

    /**
     * Update existing user
     * @param id user identifier
     * @param userData updated user information
     * @return updated user
     */
    @PutMapping("/{id}")
    public String updateUser(@PathVariable Long id, @RequestBody String userData) {
        return "Updated user " + id + " with data: " + userData;
    }
} 