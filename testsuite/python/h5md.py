#
# Copyright (C) 2013,2014,2015,2016 The ESPResSo project
#
# This file is part of ESPResSo.
#
# ESPResSo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ESPResSo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Testmodule for the H5MD interface.
"""
import os
import unittest as ut
import numpy as np
import espressomd  # pylint: disable=import-error
import h5py  # h5py has to be imported *after* espressomd (MPI)

npart=25
class CommonTests(object):
    system = espressomd.System()
    system.box_l = [npart, npart, npart] #avoid particles to be set outside of the main box, otherwise particle positions are folded in the core when writing out and we cannot directly compare positions in the dataset and where particles were set. One would need to unfold the positions of the hdf5 file.
    system.cell_system.skin = 0.4
    system.time_step = 0.01
    for i in range(npart):
        system.part.add(id=i, pos=np.array([float(i),
                                            float(i),
                                            float(i)]),
                        v=np.array([1.0, 2.0, 3.0]), type=23)
        if 'MASS' in espressomd.code_info.features():
            system.part[i].mass = 2.3
        if 'EXTERNAL_FORCE' in espressomd.code_info.features():
            system.part[i].ext_force = [0.1, 0.2, 0.3]
    system.integrator.run(steps=0)

    def test_pos(self):
        """Test if positions have been written properly."""
        self.assertTrue(np.allclose(
            np.array([(float(i), float(i), float(i)) for i in range(npart)]),
            np.array([x for (y, x) in sorted(zip(self.py_id, self.py_pos))])),
            msg="Positions not written correctly by H5md!")

    def test_vel(self):
        """Test if velocities have been written properly."""
        self.assertTrue(np.allclose(
            np.array([[1.0, 2.0, 3.0] for i in range(npart)]),
            np.array([x for (y, x) in sorted(zip(self.py_id, self.py_vel))])),
            msg="Velocities not written correctly by H5md!")

    @ut.skipIf('EXTERNAL_FORCE' not in espressomd.code_info.features(),
               "EXTERNAL_FORCE not compiled in, can not check writing forces.")
    def test_f(self):
        """Test if forces have been written properly."""
        self.assertTrue(np.allclose(
            np.array([[0.1, 0.2, 0.3] for i in range(npart)]),
            np.array([x for (y, x) in sorted(zip(self.py_id, self.py_f))])),
            msg="Forces not written correctly by H5md!")


@ut.skipIf('H5MD' not in espressomd.code_info.features(),
           "H5MD not compiled in, can not check functionality.")
class H5mdTestOrdered(ut.TestCase, CommonTests):
    """Test the core implementation of writing hdf5 files."""
    @classmethod
    def tearDownClass(cls):
        os.remove("test.h5")

    @classmethod
    def setUpClass(cls):
        write_ordered = True
        """Prepare a testsystem."""
        from espressomd.io.writer import h5md  # pylint: disable=import-error
        cls.h5 = h5md.H5md(filename="test.h5", write_pos=True, write_vel=True,
                           write_force=True, write_type=True, write_mass=True,
                           write_ordered=write_ordered)
        cls.h5.write()
        cls.h5.close()
        del cls.h5
        cls.py_file = h5py.File("test.h5", 'r')
        cls.py_pos = cls.py_file['particles/atoms/position/value']
        cls.py_vel = cls.py_file['particles/atoms/velocity/value']
        cls.py_f = cls.py_file['particles/atoms/force/value']
        cls.py_type = cls.py_file['particles/atoms/type/value']
        cls.py_mass = cls.py_file['particles/atoms/mass/value']
        cls.py_id = cls.py_file['particles/atoms/id/value']

    def test_ids(self):
        """Test if ids have been written properly."""
        self.assertTrue(np.allclose(
            np.array(range(npart)),
            self.py_id),
            msg="ids correctly ordered and written by H5md!")


class H5mdTestUnordered(ut.TestCase, CommonTests):

    @classmethod
    def tearDownClass(cls):
        os.remove("test.h5")

    @classmethod
    def setUpClass(cls):
        write_ordered = False
        """Prepare a testsystem."""
        from espressomd.io.writer import h5md  # pylint: disable=import-error
        cls.h5 = h5md.H5md(filename="test.h5", write_pos=True, write_vel=True,
                           write_force=True, write_type=True, write_mass=True,
                           write_ordered=False)
        cls.h5.write()
        cls.h5.close()
        del cls.h5
        cls.py_file = h5py.File("test.h5", 'r')
        cls.py_pos = cls.py_file['particles/atoms/position/value']
        cls.py_vel = cls.py_file['particles/atoms/velocity/value']
        cls.py_f = cls.py_file['particles/atoms/force/value']
        cls.py_type = cls.py_file['particles/atoms/type/value']
        cls.py_mass = cls.py_file['particles/atoms/mass/value']
        cls.py_id = cls.py_file['particles/atoms/id/value']


if __name__ == "__main__":
    suite = ut.TestLoader().loadTestsFromTestCase(H5mdTestUnordered)
    ut.TextTestRunner(verbosity=2).run(suite)
    suite = ut.TestLoader().loadTestsFromTestCase(H5mdTestOrdered)
    ut.TextTestRunner(verbosity=2).run(suite)
