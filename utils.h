#ifndef UTILS_H
#define UTILS_H

/* just some nice utilities... */

/* force gcc to inline and not warn about unused functions */
#ifdef INLINE
#  undef INLINE
#endif
#ifdef __GNUC__
#  define INLINE inline
#else
#  define INLINE
#endif

/* Maximum von  double a und  double b berechnen, gibt double zurueck. */
INLINE static double dmax(double a, double b) { return (a>b) ? a : b; }

/* Maximum von  double a und  double b berechnen, gibt double zurueck. */
INLINE static double dmin(double a, double b) { return (a<b) ? a : b; }

/* Wert von double x runden, gibt double zurueck. */
INLINE static double dround(double x) { return floor(x+0.5); }

/* Berechnet das Quadrat von double x, gibt double zurueck. */
INLINE static double SQR(double x) { return x*x; }

INLINE static double AS_erfc_part(double d)
{
  /* approximates exp(d^2)*erfc(d) by applying a formula from:
     Abramowitz/Stegun: Handbook of Mathematical Functions, 
     Dover (9. ed.), chapter 7 */

  static double AS_a1 =  0.254829592;
  static double AS_a2 = -0.284496736;
  static double AS_a3 =  1.421413741;
  static double AS_a4 = -1.453152027;
  static double AS_a5 =  1.061405429;
  static double AS_p  =  0.3275911;
  static double t;
  
  t = 1.0 / (1.0 + AS_p * d);
  
  return t * (AS_a1 + t * (AS_a2 + t * (AS_a3 + t * (AS_a4 + t * AS_a5) ) ) );
}

#endif
