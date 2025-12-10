# Data Model for "Create AI Textbook"

This document defines the data entities for the AI Textbook feature, based on the feature specification.

## 1. Textbook

The top-level container for all content.

-   **Fields**:
    -   `title`: String (e.g., "Physical AI & Humanoid Robotics")
    -   `modules`: Array of Module entities
-   **Relationships**:
    -   Has many Modules

## 2. Module

A logical grouping of content (e.g., ROS 2).

-   **Fields**:
    -   `title`: String (e.g., "ROS 2")
    -   `chapter`: Chapter entity
-   **Relationships**:
    -   Belongs to a Textbook
    -   Has one Chapter

## 3. Chapter

A container for lessons within a module.

-   **Fields**:
    -   `title`: String (e.g., "Introduction to ROS 2")
    -   `lessons`: Array of Lesson entities
-   **Relationships**:
    -   Belongs to a Module
    -   Has many Lessons

## 4. Lesson

A single learning unit with specific sections.

-   **Fields**:
    -   `title`: String
    -   `objectives`: Markdown text
    -   `concept_summary`: Markdown text
    -   `real_world_context`: Markdown text
    -   `activity`: Markdown text
    -   `technical_notes`: Markdown text
    -   `practice_task`: Markdown text
    -   `reflection`: Markdown text
    -   `resources`: Markdown text
-   **Relationships**:
    -   Belongs to a Chapter

## 5. Capstone Project

A culminating project that integrates knowledge from all modules.

-   **Fields**:
    -   `title`: String
    -   `description`: Markdown text
    -   `tasks`: Array of strings
-   **Relationships**:
    -   Associated with the Textbook