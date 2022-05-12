from sympy import *
import numpy as np
import copy

def ReadTheFile(FileToBeOpened):
    TheFile=open(FileToBeOpened,"r+")
    FirstLine=TheFile.readline()
    ContainsVerticesEdgesFaces=FirstLine.split(' ')
    NumberOfVertices=int(ContainsVerticesEdgesFaces[0])
    print("The Number Of Vertices are:",NumberOfVertices)
    NumberOfEdges=int(ContainsVerticesEdgesFaces[1])
    print("The Number Of Edges are:",NumberOfEdges)
    NumberOfFaces=int(ContainsVerticesEdgesFaces[2])
    print("The Number Of Faces are:",NumberOfFaces)
    TheListOfEdges=[]
    TheListOfFaces=[]
    for i in range(0,NumberOfVertices):
        Coordinate=TheFile.readline()
    for i in range(0,NumberOfEdges):
        Edge=TheFile.readline()
        EdgeToBeAdded=list(map(int,Edge.split(' ')))
        TheListOfEdges.append(EdgeToBeAdded)
    for i in range(0,NumberOfFaces):
        Face=TheFile.readline()
        FaceToBeAdded=list(map(int,Face.split(' ')))
        TheListOfFaces.append(FaceToBeAdded)
    TheReturnList=[]
    TheReturnList.append(NumberOfVertices)
    TheReturnList.append(NumberOfEdges)
    TheReturnList.append(NumberOfFaces)
    TheReturnList.append(TheListOfEdges)
    TheReturnList.append(TheListOfFaces)
    return TheReturnList

def del1Column(K, num_ver, edge_index):
    img_space = []
    temp1 = [0]*num_ver

    temp1[K[edge_index][0]-1] = -1
    temp1[K[edge_index][1]-1] = 1
    img_space.append(temp1)
    img_space = np.transpose(img_space)
    return img_space

def del2Column(K, num_edge, face_index, edgeList):
    img_space = []

    temp1 = [0]*num_edge
    edges1 = []
    for i in range(0, 3):
        edges1.append(edgeList[K[face_index][i]-1])
    edges = copy.deepcopy(edges1)
    temp1[K[face_index][0]-1] = 1
    for i in range(1, 3):
        for j in range(0, 2):
            if edges[0][j] == edges[i][0]:
                edges[0][j] = edges[i][1]
                if j == 1:
                    temp1[K[face_index][i]-1] = 1
                else:
                    temp1[K[face_index][i]-1] = -1
                break
            elif edges[0][j] == edges[i][1]:
                edges[0][j] = edges[i][0]
                if j == 1:
                    temp1[K[face_index][i]-1] = -1
                else:
                    temp1[K[face_index][i]-1] = 1
                break
    img_space.append(temp1)
    img_space = np.transpose(img_space)
    return img_space

def main():
    FileToBeOpened=input("Enter the name of the file to be read with extension:")
    TheReturnedList=ReadTheFile(FileToBeOpened)
    NumberOfVertices=TheReturnedList[0]
    NumberOfEdges=TheReturnedList[1]
    NumberOfFaces=TheReturnedList[2]
    TheListOfEdges=TheReturnedList[3]
    TheListOfFaces=TheReturnedList[4]
    TheSum=NumberOfVertices+NumberOfEdges+NumberOfFaces
    K=[]
    for i in range(0,NumberOfVertices):
        K.append(i+1)
    for i in TheListOfEdges:
        K.append(i)
    for i in TheListOfFaces:
        K.append(i)
    BettiNumbers1=[]
    BettiNumbers2=[]

    for i in range(0,3):
        BettiNumbers2.append(0)
        BettiNumbers1.append(0)

    BettiNumbers2[0]=NumberOfVertices
    BettiNumbers1[0]=NumberOfVertices
    matrix1=[]
    del1Matrix=[]
    augmentedMatrix=[]
    print("Initial Betti numbers after adding all 0-simplices...")
    print("Betti-0: ", BettiNumbers2[0])
    print("Betti-1: ", BettiNumbers2[1])
    print("Betti-2: ", BettiNumbers2[2])
    print()
    for i in range(NumberOfVertices, TheSum):
        if i in range(NumberOfVertices, NumberOfVertices+NumberOfEdges):
            print("Adding Edge: ", K[i][0],'-', K[i][1])
            k=1
            if i == NumberOfVertices:
                del1Matrix = del1Column(K, NumberOfVertices, i)
                rank_matrix = 1
                rank_augmentedMatrix = 2
            else:
                matrix1 = del1Column(K, NumberOfVertices, i)
                augmentedMatrix = np.column_stack((del1Matrix, matrix1))
                rank_matrix = np.linalg.matrix_rank(del1Matrix)
                rank_augmentedMatrix = np.linalg.matrix_rank(augmentedMatrix)
                del1Matrix = np.column_stack((del1Matrix, matrix1))
        else:
            print("Adding Face: ", K[i][0],'-', K[i][1],'-', K[i][2])
            k=2
            if i == NumberOfVertices+NumberOfEdges:
                del1Matrix = del2Column(K, NumberOfEdges, i, TheListOfEdges)
                rank_matrix = 1
                rank_augmentedMatrix = 2
            else:
                matrix1 = del2Column(K, NumberOfEdges, i, TheListOfEdges)
                augmentedMatrix = np.column_stack((del1Matrix, matrix1))
                rank_matrix = np.linalg.matrix_rank(del1Matrix)
                rank_augmentedMatrix = np.linalg.matrix_rank(augmentedMatrix)
                del1Matrix = np.column_stack((del1Matrix, matrix1))

        if rank_matrix == rank_augmentedMatrix:
            for p in range(0, k+1):
                if p == k:
                    BettiNumbers2[p] = BettiNumbers1[p]+1
                else:
                    BettiNumbers2[p] = BettiNumbers1[p]
                BettiNumbers1[p] = BettiNumbers2[p]
        else:
            for p in range(0, k+1):
                if p == k-1:
                    BettiNumbers2[p] = BettiNumbers1[p]-1
                else:
                    BettiNumbers2[p] = BettiNumbers1[p]
                BettiNumbers1[p] = BettiNumbers2[p]
        print("Betti-0: ", BettiNumbers2[0])
        print("Betti-1: ", BettiNumbers2[1])
        print("Betti-2: ", BettiNumbers2[2])
        print()

    print("Final Result...")
    print("Betti-0: ", BettiNumbers2[0])
    print("Betti-1: ", BettiNumbers2[1])
    print("Betti-2: ", BettiNumbers2[2])
main()