#ifndef IS_SEQ_H
#define IS_SEQ_H


// Slope-reuse Interpolation Search - SIP
template <int record_bytes>
class is_seq {
  using Vector = PaddedVector<record_bytes>;
  using Linear = LinearUnroll<Vector>;

  const Vector &data;

  /////// Interpolator /////////////////////////
  const FixedPoint slope;
  const double f_aL;
  const double f_width_range;

  Index interpolate(const Key x, const Index mid, bool approx = true) {
    return approx ? (x < data[mid] ? mid - slope * (uint64_t)(data[mid] - x)
                                   : mid + slope * (uint64_t)(x - data[mid]))
                  : mid + (Index)(((double)x - (double)data[mid])
                    * f_width_range);
  }

  Index interpolate(const Key x, bool approx = true) {
    return approx ? slope * (uint64_t)(x - data[0])
                  : (Index)(((double)x - f_aL) * f_width_range);
  }

  //////////////////////////////////////////////
 public:
  is_seq(const Vector &data)
      : data(data),
        slope(FixedPoint::Gen(data.size() - 1) / (data.back() - data[0])),
        f_aL(data[0]),
        f_width_range((double)((uint64_t)data.size() - 1) /
            (double)(data.back() - data[0]))
  {}

  __attribute__((always_inline)) Key search(const Key x) {
    assert(data.size() >= 1);
    // set bounds and do first interpolation
    Index left = 0, right = data.size() - 1, next = interpolate(x);

    // update bounds and check for match
    if (data[next] < x)
      left = next + 1;
    else if (data[next] > x)
      right = next - 1;
    else
      return data[next];
    if (left == right)
      return data[left];

    // next interpolation
    assert(left < right);
    assert(left >= 0);
    assert(right < data.size());
    next = interpolate(x, next);

    // linear search base case
    if (data[next] >= x) {
      return data[Linear::reverse(data, next, x)];
    } else {
      return data[Linear::forward(data, next + 1, x)];
    }

    return 0;
  }
};

#endif //IS_SEQ_H