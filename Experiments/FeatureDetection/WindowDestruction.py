import cv2


class WindowDestruction:

    @classmethod
    def windowDestroyer(self, numberOfFramesOpen):
        totalFrames = numberOfFramesOpen * 4        # Every frame takes 4 wait keys.
        totalFrames = totalFrames + 1               # Everything is 0 indexed, so we gotta add 1 bad boy on there.
        cv2.destroyAllWindows()
        for i in range(1, totalFrames):
            cv2.waitKey(1)
