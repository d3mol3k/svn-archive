
global_settings {
    assumed_gamma 2.0
    noise_generator 2
}

camera {
   orthographic
   location <0, 10000, 0>
   sky <0, 1, 0>
   direction <0, 0, 1>
   right <1.05881055874*568.50385331, 0, 0>
   up <0, 1*568.50385331*cos(radians(10)), 0> /* this stretches in y to compensate for the rotate below */
   look_at <0, 0, 0>
   rotate <-10,0,0>
   scale <1,1,1>
   translate <1109383.14489,0,6420134.71535>
}

/* ground */
box {
    <1109082.17595, -0.5, 6419850.46342>, <1109684.11383, -0.0, 6420418.96728>
    pigment {
        color rgb <1, 1, 1>
    }
    finish {
        ambient 1
    }
}
prism { linear_spline  0, 0.01, 53,
/* osm_id=29395745 */
  <1107181.31, 6421608.96>,
  <1107383.67, 6421979.88>,
  <1108189.12, 6422340.56>,
  <1108491.75, 6422477.67>,
  <1108759.9, 6422581.67>,
  <1108908.69, 6422226.59>,
  <1109348.51, 6422409.2>,
  <1109794.87, 6422054.11>,
  <1109598.37, 6421608.27>,
  <1109530.19, 6421438.55>,
  <1109536.21, 6421401.31>,
  <1109549.35, 6421349.32>,
  <1109565.97, 6421300.88>,
  <1109783.43, 6420765.8>,
  <1109558.6, 6420472.07>,
  <1109534.36, 6420440.85>,
  <1109347.42, 6420553.25>,
  <1109348.04, 6420531.51>,
  <1109327.33, 6420471.08>,
  <1109253.66, 6420325.65>,
  <1109209.21, 6420185.89>,
  <1109206.16, 6420151.88>,
  <1109207.38, 6420109.4>,
  <1109215.3, 6420069.74>,
  <1109311.5, 6419834.59>,
  <1109427.19, 6419534.32>,
  <1109472.26, 6419397.41>,
  <1109538.01, 6419292.59>,
  <1109569.07, 6419260.48>,
  <1109598.9, 6419237.84>,
  <1109520.36, 6419171.74>,
  <1109418.06, 6419375.69>,
  <1109364.48, 6419529.61>,
  <1109218.95, 6419531.49>,
  <1109212.86, 6419591.93>,
  <1109049.67, 6419778.88>,
  <1108972.34, 6419709>,
  <1108894.4, 6419786.45>,
  <1108663.62, 6420032.9>,
  <1108590.55, 6420139.61>,
  <1108506.23, 6420238.55>,
  <1108506.94, 6420315.98>,
  <1108506.97, 6420319.12>,
  <1108549.99, 6420355.71>,
  <1108500.44, 6420460.69>,
  <1108456.76, 6420531.68>,
  <1108577.01, 6420580.11>,
  <1108541.46, 6420676.66>,
  <1108316.01, 6420581.68>,
  <1108207.18, 6420854.59>,
  <1107730.49, 6420678.78>,
  <1107593.16, 6420841.14>,
  <1107181.31, 6421608.96>

    texture {
        pigment {
            color rgb <1,0.95,0.9>
        }
        finish {
            ambient 1
            /*specular 0.5
            roughness 0.05
            reflection 0.5*/
        }
    }
}

prism { linear_spline  0, 0.01, 16,
/* osm_id=29080816 */
  <1109221.21, 6420142.63>,
  <1109226.23, 6420181.02>,
  <1109239.51, 6420233.34>,
  <1109323.29, 6420201.41>,
  <1109351.43, 6420220.82>,
  <1109387.64, 6420302.5>,
  <1109473.92, 6420267.31>,
  <1109517.56, 6420281.88>,
  <1109600.73, 6420123.45>,
  <1109654.21, 6420041.55>,
  <1109610.35, 6420010.84>,
  <1109553.52, 6420095.5>,
  <1109275.74, 6419960.08>,
  <1109240.22, 6420039.12>,
  <1109223, 6420104.22>,
  <1109221.21, 6420142.63>

    texture {
        pigment {
            color rgb <1,1,0.9>
        }
        finish {
            ambient 1
            /*specular 0.5
            roughness 0.05
            reflection 0.5*/
        }
    }
}

prism { linear_spline  0, 0.01, 19,
/* osm_id=29395746 */
  <1109297.67, 6419926.87>,
  <1109357.41, 6419954.37>,
  <1109338.81, 6419989.45>,
  <1109467.57, 6420051.53>,
  <1109514.35, 6419957.35>,
  <1109614.93, 6420002.38>,
  <1109679.53, 6419886.69>,
  <1109556.05, 6419817.92>,
  <1109707.73, 6419381.03>,
  <1109724.66, 6419344.64>,
  <1109731.73, 6419328.03>,
  <1109667.52, 6419292.07>,
  <1109646.2, 6419286.93>,
  <1109602.19, 6419264.23>,
  <1109548.22, 6419324.34>,
  <1109488.22, 6419426.82>,
  <1109445.61, 6419549.55>,
  <1109409.08, 6419634.51>,
  <1109297.67, 6419926.87>

    texture {
        pigment {
            color rgb <1,1,0.9>
        }
        finish {
            ambient 1
            /*specular 0.5
            roughness 0.05
            reflection 0.5*/
        }
    }
}

