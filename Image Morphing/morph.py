# Imports
import numpy as np
import cv2
from imutils import face_utils
import dlib

# Face morpher class
class FaceMorpher:

    # Constructor which defines alpha for which one of the source images the destination should look closer to
    def __init__(self, alpha=0.5):
        self.alpha = alpha
        self.landmarkPredictor = 'shape_predictor_68_face_landmarks.dat'

    # Resizing an image to 600 width and 800 height
    def resizeImage(self, filename):
        image = cv2.imread(filename)
        resizedImage = cv2.resize(image, (600, 800))
        cv2.imwrite(filename + "_resize.jpg", resizedImage)

    # Detects landmarks in the two source images for facial features such eyes, nose, etc as (x,y) coordinates
    def landmarkDetection(self, filename, points):
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(self.landmarkPredictor)
        image = cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)

        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            for (x, y) in shape:
                points.append((int(x), int(y)))

    # Performs delaunlays traingulation and gets all the triangle indexes given a set of points
    def delaunayDivision(self, img, points):
        area2D = cv2.Subdiv2D((0, 0, img.shape[1], img.shape[0]))

        for p in points:
            area2D.insert(p)

        tlist = area2D.getTriangleList()
        finalList = []
        for tri in tlist:
            k = [0, 0, 0]
            for i in range(0, 6, 2):
                for index, pt in enumerate(points):
                    if pt[0] == tri[i] and pt[1] == tri[i + 1]:
                        k[int(i / 2)] = index

            finalList.append(k)
        return finalList

    # Affine transformation to morph two triangles in different images. Used for blending two images
    @staticmethod
    def affine(rectWithoutMask, sourceTriangle, morphedTriangle, size):
        interWarp = cv2.getAffineTransform(np.float32(sourceTriangle), np.float32(morphedTriangle))
        finalWarp = cv2.warpAffine(rectWithoutMask, interWarp, (size[0], size[1]),
                                   None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
        return finalWarp

    # Morphing the triangle given the source and destination
    def blendTriangle(self, srcImg1, srcImg2, warpImg, t1Vertices, t2Vertices, morphedT):
        
        # Creating bouding boxes over the triangles of the two sources and one destination
        r1 = cv2.boundingRect(np.float32([t1Vertices]))
        r2 = cv2.boundingRect(np.float32([t2Vertices]))
        r = cv2.boundingRect(np.float32([morphedT]))

        # Offsetting the triangles by the top left corner point of the rectangle given above for each of the triangles
        t1VerticesRect = [(t[0] - r1[0], t[1] - r1[1]) for t in t1Vertices]
        t2VerticesRect = [(t[0] - r2[0], t[1] - r2[1]) for t in t2Vertices]
        morphedTRect = [(t[0] - r[0], t[1] - r[1]) for t in morphedT]

        # Creating a mask of the rectangle
        mask = np.zeros((r[3], r[2], 3), dtype=np.float32)
        cv2.fillConvexPoly(mask, np.int32(morphedTRect), (1.0, 1.0, 1.0), 16, 0)

        # Creating the image without the mask
        srcImg1Rect = srcImg1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
        srcImg2Rect = srcImg2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

        # Performing affine transformation on the bounded rectangles.
        size = (r[2], r[3])
        warpImage1 = self.affine(srcImg1Rect, t1VerticesRect, morphedTRect, size)
        warpImage2 = self.affine(srcImg2Rect, t2VerticesRect, morphedTRect, size)

        # Taking alpha of one source image and 1-alpha of the other source image
        imgRect = (1.0 - self.alpha) * warpImage1 + self.alpha * warpImage2

        # Warping the image and adding the blended region to the mask
        warpImg[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] = warpImg[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] * (1 - mask) + imgRect * mask


# Client
if __name__ == "__main__":
    
    filename1 = "pic1.jpg"
    filename2 = "pic2.jpg"

    morpher = FaceMorpher(alpha=0.67)

    morpher.resizeImage(filename1)
    morpher.resizeImage(filename2)

    filename1 = filename1 + "_resize.jpg"
    filename2 = filename2 + "_resize.jpg"

    points1 = []
    points2 = []

    morpher.landmarkDetection(filename1, points1)
    morpher.landmarkDetection(filename2, points2)

    img1 = cv2.imread(filename1)
    img2 = cv2.imread(filename2)

    img1 = np.float32(img1)
    img2 = np.float32(img2)

    delaunay = morpher.delaunayDivision(img1, points1)

    points = []

    for i in range(0, len(points1)):
        x = (1 - morpher.alpha) * points1[i][0] + morpher.alpha * points2[i][0]
        y = (1 - morpher.alpha) * points1[i][1] + morpher.alpha * points2[i][1]
        points.append((x, y))

    imgMorph = np.zeros(img1.shape, dtype=img1.dtype)

    for v1, v2, v3 in delaunay:
        t1 = [points1[v1], points1[v2], points1[v3]]
        t2 = [points2[v1], points2[v2], points2[v3]]
        t = [points[v1], points[v2], points[v3]]
        morpher.blendTriangle(img1, img2, imgMorph, t1, t2, t)

    cv2.imshow("Morphed Face", np.uint8(imgMorph))
    cv2.waitKey(0)