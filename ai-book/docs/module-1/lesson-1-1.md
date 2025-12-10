---
title: "Lesson 1.1: Introduction to ROS 2"
---

# Lesson 1.1: Introduction to ROS 2

## Objectives

- Understand the core concepts of ROS 2, including nodes, topics, and messages.
- Learn how to create a ROS 2 workspace and a simple Python package.
- Write a "hello world" publisher and subscriber in Python.
- Run and observe the communication between the two nodes.

## Concept Summary

ROS (Robot Operating System) is a flexible framework for writing robot software. ROS 2 is the second generation of ROS, with improvements in performance, security, and support for multi-robot systems.

- **Nodes**: A node is an executable that uses ROS to communicate with other nodes.
- **Topics**: Nodes can publish messages to a topic as well as subscribe to a topic to receive messages.
- **Messages**: When a node sends data on a topic, it uses a message. Messages are a simple data structure, containing typed fields.

## Real-World Context

ROS 2 is used in a wide variety of robotics applications, from self-driving cars and industrial manipulators to autonomous drones and research platforms. Understanding ROS 2 is a fundamental skill for any robotics engineer.

## Activity: "Hello World" Publisher and Subscriber

In this activity, you will create two nodes: one that publishes a "hello world" message and another that subscribes to that message and prints it to the console.

## Technical Notes

- You will need to have ROS 2 installed on your system.
- Make sure to source your ROS 2 setup file before running any commands.
- The package `rclpy` is the Python client library for ROS 2.

## Practice Task

Modify the publisher to send a message with your name, and modify the subscriber to print a greeting to you.

## Reflection

- What other types of messages could be sent between nodes?
- How could you use nodes and topics to control a simple robot?

## Resources

- [ROS 2 Documentation](https://docs.ros.org/en/foxy/index.html)
- [rclpy API Documentation](https://docs.ros2.org/foxy/api/rclpy/index.html)