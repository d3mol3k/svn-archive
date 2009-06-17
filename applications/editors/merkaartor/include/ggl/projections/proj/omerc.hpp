#ifndef GGL_PROJECTIONS_OMERC_HPP
#define GGL_PROJECTIONS_OMERC_HPP

// Generic Geometry Library - projections (based on PROJ4)
// This file is automatically generated. DO NOT EDIT.

// Copyright Barend Gehrels (1995-2009), Geodan Holding B.V. Amsterdam, the Netherlands.
// Copyright Bruno Lalande (2008-2009)
// Use, modification and distribution is subject to the Boost Software License,
// Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

// This file is converted from PROJ4, http://trac.osgeo.org/proj
// PROJ4 is originally written by Gerald Evenden (then of the USGS)
// PROJ4 is maintained by Frank Warmerdam
// PROJ4 is converted to Geometry Library by Barend Gehrels (Geodan, Amsterdam)

// Original copyright notice:

// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the "Software"),
// to deal in the Software without restriction, including without limitation
// the rights to use, copy, modify, merge, publish, distribute, sublicense,
// and/or sell copies of the Software, and to permit persons to whom the
// Software is furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included
// in all copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
// OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
// THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
// DEALINGS IN THE SOFTWARE.

#include <ggl/projections/impl/base_static.hpp>
#include <ggl/projections/impl/base_dynamic.hpp>
#include <ggl/projections/impl/projects.hpp>
#include <ggl/projections/impl/factory_entry.hpp>
#include <ggl/projections/impl/pj_tsfn.hpp>
#include <ggl/projections/impl/pj_phi2.hpp>

namespace ggl { namespace projection
{
    #ifndef DOXYGEN_NO_IMPL
    namespace impl { namespace omerc{
            static const double TOL = 1.e-7;
            static const double EPS = 1.e-10;

                inline double TSFN0(double x)
                    {return tan(.5 * (HALFPI - (x))); }


            struct par_omerc
            {
                double alpha, lamc, lam1, phi1, lam2, phi2, Gamma, al, bl, el,
                singam, cosgam, sinrot, cosrot, u_0;
                int  ellips, rot;
            };

            // template class, using CRTP to implement forward/inverse
            template <typename LatLong, typename Cartesian, typename Parameters>
            struct base_omerc_ellipsoid : public base_t_fi<base_omerc_ellipsoid<LatLong, Cartesian, Parameters>, LatLong, Cartesian, Parameters>
            {

                typedef typename base_t_fi<base_omerc_ellipsoid<LatLong, Cartesian, Parameters>, LatLong, Cartesian, Parameters>::LL_T LL_T;
                typedef typename base_t_fi<base_omerc_ellipsoid<LatLong, Cartesian, Parameters>, LatLong, Cartesian, Parameters>::XY_T XY_T;

                par_omerc m_proj_parm;

                inline base_omerc_ellipsoid(const Parameters& par)
                    : base_t_fi<base_omerc_ellipsoid<LatLong, Cartesian, Parameters>, LatLong, Cartesian, Parameters>(*this, par) {}

                inline void fwd(LL_T& lp_lon, LL_T& lp_lat, XY_T& xy_x, XY_T& xy_y) const
                {
                    double  con, q, s, ul, us, vl, vs;

                    vl = sin(this->m_proj_parm.bl * lp_lon);
                    if (fabs(fabs(lp_lat) - HALFPI) <= EPS) {
                        ul = lp_lat < 0. ? -this->m_proj_parm.singam : this->m_proj_parm.singam;
                        us = this->m_proj_parm.al * lp_lat / this->m_proj_parm.bl;
                    } else {
                        q = this->m_proj_parm.el / (this->m_proj_parm.ellips ? pow(pj_tsfn(lp_lat, sin(lp_lat), this->m_par.e), this->m_proj_parm.bl)
                            : TSFN0(lp_lat));
                        s = .5 * (q - 1. / q);
                        ul = 2. * (s * this->m_proj_parm.singam - vl * this->m_proj_parm.cosgam) / (q + 1. / q);
                        con = cos(this->m_proj_parm.bl * lp_lon);
                        if (fabs(con) >= TOL) {
                            us = this->m_proj_parm.al * atan((s * this->m_proj_parm.cosgam + vl * this->m_proj_parm.singam) / con) / this->m_proj_parm.bl;
                            if (con < 0.)
                                us += PI * this->m_proj_parm.al / this->m_proj_parm.bl;
                        } else
                            us = this->m_proj_parm.al * this->m_proj_parm.bl * lp_lon;
                    }
                    if (fabs(fabs(ul) - 1.) <= EPS) throw proj_exception();;
                    vs = .5 * this->m_proj_parm.al * log((1. - ul) / (1. + ul)) / this->m_proj_parm.bl;
                    us -= this->m_proj_parm.u_0;
                    if (! this->m_proj_parm.rot) {
                        xy_x = us;
                        xy_y = vs;
                    } else {
                        xy_x = vs * this->m_proj_parm.cosrot + us * this->m_proj_parm.sinrot;
                        xy_y = us * this->m_proj_parm.cosrot - vs * this->m_proj_parm.sinrot;
                    }
                }

                inline void inv(XY_T& xy_x, XY_T& xy_y, LL_T& lp_lon, LL_T& lp_lat) const
                {
                    double  q, s, ul, us, vl, vs;

                    if (! this->m_proj_parm.rot) {
                        us = xy_x;
                        vs = xy_y;
                    } else {
                        vs = xy_x * this->m_proj_parm.cosrot - xy_y * this->m_proj_parm.sinrot;
                        us = xy_y * this->m_proj_parm.cosrot + xy_x * this->m_proj_parm.sinrot;
                    }
                    us += this->m_proj_parm.u_0;
                    q = exp(- this->m_proj_parm.bl * vs / this->m_proj_parm.al);
                    s = .5 * (q - 1. / q);
                    vl = sin(this->m_proj_parm.bl * us / this->m_proj_parm.al);
                    ul = 2. * (vl * this->m_proj_parm.cosgam + s * this->m_proj_parm.singam) / (q + 1. / q);
                    if (fabs(fabs(ul) - 1.) < EPS) {
                        lp_lon = 0.;
                        lp_lat = ul < 0. ? -HALFPI : HALFPI;
                    } else {
                        lp_lat = this->m_proj_parm.el / sqrt((1. + ul) / (1. - ul));
                        if (this->m_proj_parm.ellips) {
                            if ((lp_lat = pj_phi2(pow(lp_lat, 1. / this->m_proj_parm.bl), this->m_par.e)) == HUGE_VAL)
                                throw proj_exception();;
                        } else
                            lp_lat = HALFPI - 2. * atan(lp_lat);
                        lp_lon = - atan2((s * this->m_proj_parm.cosgam -
                            vl * this->m_proj_parm.singam), cos(this->m_proj_parm.bl * us / this->m_proj_parm.al)) / this->m_proj_parm.bl;
                    }
                }
            };

            // Oblique Mercator
            template <typename Parameters>
            void setup_omerc(Parameters& par, par_omerc& proj_parm)
            {
                double con, com, cosph0, d, f, h, l, sinph0, p, j;
                int azi;
                proj_parm.rot    = pj_param(par.params, "bno_rot").i == 0;
                if( (azi    = pj_param(par.params, "talpha").i) != 0.0) {
                    proj_parm.lamc    = pj_param(par.params, "rlonc").f;
                    proj_parm.alpha    = pj_param(par.params, "ralpha").f;
                    if ( fabs(proj_parm.alpha) <= TOL ||
                        fabs(fabs(par.phi0) - HALFPI) <= TOL ||
                        fabs(fabs(proj_parm.alpha) - HALFPI) <= TOL)
                        throw proj_exception(-32);
                } else {
                    proj_parm.lam1    = pj_param(par.params, "rlon_1").f;
                    proj_parm.phi1    = pj_param(par.params, "rlat_1").f;
                    proj_parm.lam2    = pj_param(par.params, "rlon_2").f;
                    proj_parm.phi2    = pj_param(par.params, "rlat_2").f;
                    if (fabs(proj_parm.phi1 - proj_parm.phi2) <= TOL ||
                        (con = fabs(proj_parm.phi1)) <= TOL ||
                        fabs(con - HALFPI) <= TOL ||
                        fabs(fabs(par.phi0) - HALFPI) <= TOL ||
                        fabs(fabs(proj_parm.phi2) - HALFPI) <= TOL) throw proj_exception(-33);
                }
                com = (proj_parm.ellips = par.es > 0.) ? sqrt(par.one_es) : 1.;
                if (fabs(par.phi0) > EPS) {
                    sinph0 = sin(par.phi0);
                    cosph0 = cos(par.phi0);
                    if (proj_parm.ellips) {
                        con = 1. - par.es * sinph0 * sinph0;
                        proj_parm.bl = cosph0 * cosph0;
                        proj_parm.bl = sqrt(1. + par.es * proj_parm.bl * proj_parm.bl / par.one_es);
                        proj_parm.al = proj_parm.bl * par.k0 * com / con;
                        d = proj_parm.bl * com / (cosph0 * sqrt(con));
                    } else {
                        proj_parm.bl = 1.;
                        proj_parm.al = par.k0;
                        d = 1. / cosph0;
                    }
                    if ((f = d * d - 1.) <= 0.)
                        f = 0.;
                    else {
                        f = sqrt(f);
                        if (par.phi0 < 0.)
                            f = -f;
                    }
                    proj_parm.el = f += d;
                    if (proj_parm.ellips)    proj_parm.el *= pow(pj_tsfn(par.phi0, sinph0, par.e), proj_parm.bl);
                    else        proj_parm.el *= TSFN0(par.phi0);
                } else {
                    proj_parm.bl = 1. / com;
                    proj_parm.al = par.k0;
                    proj_parm.el = d = f = 1.;
                }
                if (azi) {
                    proj_parm.Gamma = asin(sin(proj_parm.alpha) / d);
                    par.lam0 = proj_parm.lamc - asin((.5 * (f - 1. / f)) *
                       tan(proj_parm.Gamma)) / proj_parm.bl;
                } else {
                    if (proj_parm.ellips) {
                        h = pow(pj_tsfn(proj_parm.phi1, sin(proj_parm.phi1), par.e), proj_parm.bl);
                        l = pow(pj_tsfn(proj_parm.phi2, sin(proj_parm.phi2), par.e), proj_parm.bl);
                    } else {
                        h = TSFN0(proj_parm.phi1);
                        l = TSFN0(proj_parm.phi2);
                    }
                    f = proj_parm.el / h;
                    p = (l - h) / (l + h);
                    j = proj_parm.el * proj_parm.el;
                    j = (j - l * h) / (j + l * h);
                    if ((con = proj_parm.lam1 - proj_parm.lam2) < -PI)
                        proj_parm.lam2 -= TWOPI;
                    else if (con > PI)
                        proj_parm.lam2 += TWOPI;
                    par.lam0 = adjlon(.5 * (proj_parm.lam1 + proj_parm.lam2) - atan(
                       j * tan(.5 * proj_parm.bl * (proj_parm.lam1 - proj_parm.lam2)) / p) / proj_parm.bl);
                    proj_parm.Gamma = atan(2. * sin(proj_parm.bl * adjlon(proj_parm.lam1 - par.lam0)) /
                       (f - 1. / f));
                    proj_parm.alpha = asin(d * sin(proj_parm.Gamma));
                }
                proj_parm.singam = sin(proj_parm.Gamma);
                proj_parm.cosgam = cos(proj_parm.Gamma);
                f = pj_param(par.params, "brot_conv").i ? proj_parm.Gamma : proj_parm.alpha;
                proj_parm.sinrot = sin(f);
                proj_parm.cosrot = cos(f);
                proj_parm.u_0 = pj_param(par.params, "bno_uoff").i ? 0. :
                    fabs(proj_parm.al * atan(sqrt(d * d - 1.) / proj_parm.cosrot) / proj_parm.bl);
                if (par.phi0 < 0.)
                    proj_parm.u_0 = - proj_parm.u_0;
                // par.inv = e_inverse;
                // par.fwd = e_forward;
            }

        }} // namespace impl::omerc
    #endif // doxygen

    /*!
        \brief Oblique Mercator projection
        \ingroup projections
        \tparam LatLong latlong point type
        \tparam Cartesian xy point type
        \tparam Parameters parameter type
        \par Projection characteristics
         - Cylindrical
         - Spheroid
         - Ellipsoid
         - no_rot rot_conv no_uoff and
         - alpha= lonc= or
         - lon_1= lat_1= lon_2= lat_2=
        \par Example
        \image html ex_omerc.gif
    */
    template <typename LatLong, typename Cartesian, typename Parameters = parameters>
    struct omerc_ellipsoid : public impl::omerc::base_omerc_ellipsoid<LatLong, Cartesian, Parameters>
    {
        inline omerc_ellipsoid(const Parameters& par) : impl::omerc::base_omerc_ellipsoid<LatLong, Cartesian, Parameters>(par)
        {
            impl::omerc::setup_omerc(this->m_par, this->m_proj_parm);
        }
    };

    #ifndef DOXYGEN_NO_IMPL
    namespace impl
    {

        // Factory entry(s)
        template <typename LatLong, typename Cartesian, typename Parameters>
        class omerc_entry : public impl::factory_entry<LatLong, Cartesian, Parameters>
        {
            public :
                virtual projection<LatLong, Cartesian>* create_new(const Parameters& par) const
                {
                    return new base_v_fi<omerc_ellipsoid<LatLong, Cartesian, Parameters>, LatLong, Cartesian, Parameters>(par);
                }
        };

        template <typename LatLong, typename Cartesian, typename Parameters>
        inline void omerc_init(impl::base_factory<LatLong, Cartesian, Parameters>& factory)
        {
            factory.add_to_factory("omerc", new omerc_entry<LatLong, Cartesian, Parameters>);
        }

    } // namespace impl
    #endif // doxygen

}} // namespace ggl::projection

#endif // GGL_PROJECTIONS_OMERC_HPP

