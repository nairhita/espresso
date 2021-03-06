/*
  Copyright (C) 2010,2011,2012,2013,2014 The ESPResSo project
  Copyright (C) 2002,2003,2004,2005,2006,2007,2008,2009,2010
  Max-Planck-Institute for Polymer Research, Theory Group

  This file is part of ESPResSo.

  ESPResSo is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  ESPResSo is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef SCRIPT_INTERFACE_SHAPES_RHOMBOID_HPP
#define SCRIPT_INTERFACE_SHAPES_RHOMBOID_HPP

#include "Shape.hpp"
#include "core/shapes/Rhomboid.hpp"

namespace ScriptInterface {
namespace Shapes {

class Rhomboid : public Shape {
public:
  Rhomboid() : m_rhomboid(new ::Shapes::Rhomboid()) {}

  const std::string name() const override { return "Shapes::Rhomboid"; }

  ParameterMap valid_parameters() const override;
  VariantMap get_parameters() const override;
  void set_parameter(const std::string &name, const Variant &value) override;

  std::shared_ptr<::Shapes::Shape> shape() const override { return m_rhomboid; }

private:
  std::shared_ptr<::Shapes::Rhomboid> m_rhomboid;
};

} /* namespace Shapes */
} /* namespace ScriptInterface */

#endif
