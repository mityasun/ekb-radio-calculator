import { IntervalPrice, TimeInterval } from 'shared/types';

export const getTimeIntervals = (intervalPrice: IntervalPrice[]): TimeInterval[] => {
  return intervalPrice
    .map((item) => {
      return {
        id: item.time_interval.id,
        time_interval: item.time_interval.time_interval
      };
    })
    .filter(
      (value, index, self) =>
        self.findIndex((item) => item.id === value.id && item.time_interval === value.time_interval) === index
    );
};
