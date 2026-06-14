                    fingers.append(1)
                else:
                    fingers.append(0)

            finger_count = sum(fingers)

    # Show number
    cv2.putText(
        frame,
        f'Fingers: {finger_count}',
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        4
    )

    cv2.imshow("Hand Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
