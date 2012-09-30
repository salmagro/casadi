#
#     This file is part of CasADi.
# 
#     CasADi -- A symbolic framework for dynamic optimization.
#     Copyright (C) 2010 by Joel Andersson, Moritz Diehl, K.U.Leuven. All rights reserved.
# 
#     CasADi is free software; you can redistribute it and/or
#     modify it under the terms of the GNU Lesser General Public
#     License as published by the Free Software Foundation; either
#     version 3 of the License, or (at your option) any later version.
# 
#     CasADi is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#     Lesser General Public License for more details.
# 
#     You should have received a copy of the GNU Lesser General Public
#     License along with CasADi; if not, write to the Free Software
#     Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
# 
# 
from casadi import *
import casadi as c
from numpy import *
import unittest
from types import *
from helpers import *

qpsolvers = []
try:
  qpsolvers.append(IpoptQPSolver)
except:
  pass
try:
  qpsolvers.append(OOQPSolver)
except:
  pass
try:
  qpsolvers.append(QPOasesSolver)
except:
  pass

class QPSolverTests(casadiTestCase):

  def test_general_convex(self):
  
    H = DMatrix([[1,-1],[-1,2]])
    G = DMatrix([-2,-6])
    A =  DMatrix([[1, 1],[-1, 2],[2, 1]])
    UBA = DMatrix([2, 2, 3])
    LBA = DMatrix([-inf]*3)

    LBX = DMatrix([0]*2)
    UBX = DMatrix([inf]*2)

    options = {"convex": True, "mutol": 1e-12, "artol": 1e-12, "tol":1e-12}
      
    for qpsolver in qpsolvers:
      self.message("general_convex: " + str(qpsolver))

      solver = qpsolver(H.sparsity(),A.sparsity())
      for key, val in options.iteritems():
        if solver.hasOption(key):
           solver.setOption(key,val)
      solver.init()

      solver.input(QP_H).set(H)
      solver.input(QP_G).set(G)
      solver.input(QP_A).set(A)
      solver.input(QP_LBX).set(LBX)
      solver.input(QP_UBX).set(UBX)
      solver.input(QP_LBA).set(LBA)
      solver.input(QP_UBA).set(UBA)

      solver.solve()

      self.assertAlmostEqual(solver.output()[0],2.0/3,6,str(qpsolver))
      self.assertAlmostEqual(solver.output()[1],4.0/3,6,str(qpsolver))
    
      self.assertAlmostEqual(solver.output(QP_LAMBDA_X)[0],0,6,str(qpsolver))
      self.assertAlmostEqual(solver.output(QP_LAMBDA_X)[1],0,6,str(qpsolver))

      self.assertAlmostEqual(solver.output(QP_LAMBDA_A)[0],3+1.0/9,6,str(qpsolver))
      self.assertAlmostEqual(solver.output(QP_LAMBDA_A)[1],4.0/9,6,str(qpsolver))
      
      self.assertAlmostEqual(solver.output(QP_COST)[0],-8-2.0/9,6,str(qpsolver))
      
      solver.input(QP_H).set(H*4)

      solver.evaluate()
      self.assertAlmostEqual(solver.output()[0],1,6,str(qpsolver))
      self.assertAlmostEqual(solver.output()[1],1,6,str(qpsolver))
      self.assertAlmostEqual(solver.output(QP_COST),-6,6,str(qpsolver))
      
      self.assertAlmostEqual(solver.output(QP_LAMBDA_X)[0],0,6,str(qpsolver))
      self.assertAlmostEqual(solver.output(QP_LAMBDA_X)[1],0,6,str(qpsolver))

      self.assertAlmostEqual(solver.output(QP_LAMBDA_A)[0],2,4,str(qpsolver))
      self.assertAlmostEqual(solver.output(QP_LAMBDA_A)[1],0,6,str(qpsolver))
      
      solver.input(QP_H).set(0)

      solver.evaluate()
      self.assertAlmostEqual(solver.output()[0],2.0/3,6,str(qpsolver))
      self.assertAlmostEqual(solver.output()[1],4.0/3,6,str(qpsolver))
      self.assertAlmostEqual(solver.output(QP_COST),-9-1.0/3,6,str(qpsolver))
      
      self.assertAlmostEqual(solver.output(QP_LAMBDA_X)[0],0,6,str(qpsolver))
      self.assertAlmostEqual(solver.output(QP_LAMBDA_X)[1],0,6,str(qpsolver))

      self.assertAlmostEqual(solver.output(QP_LAMBDA_A)[0],10.0/3,4,str(qpsolver))
      self.assertAlmostEqual(solver.output(QP_LAMBDA_A)[1],4.0/3,6,str(qpsolver))
      
      solver.input(QP_LBA).set([-inf]*3)
      solver.input(QP_UBA).set([inf]*3)

      solver.input(QP_UBX).setAll(5)

      if not('OOQP' in str(qpsolver)): # bug?
        solver.evaluate()
        self.assertAlmostEqual(solver.output()[0],5,6,str(qpsolver))
        self.assertAlmostEqual(solver.output()[1],5,6,str(qpsolver))
        self.assertAlmostEqual(solver.output(QP_COST),-40,5,str(qpsolver))
        
        self.assertAlmostEqual(solver.output(QP_LAMBDA_X)[0],2,6,str(qpsolver))
        self.assertAlmostEqual(solver.output(QP_LAMBDA_X)[1],6,6,str(qpsolver))

        self.assertAlmostEqual(solver.output(QP_LAMBDA_A)[0],0,4,str(qpsolver))
        self.assertAlmostEqual(solver.output(QP_LAMBDA_A)[1],0,6,str(qpsolver))
      
      #solver.input(QP_UBA).set([-inf]*3)
      
      #self.assertRaises(Exception,lambda : solver.evaluate())
      
    
if __name__ == '__main__':
    unittest.main()
