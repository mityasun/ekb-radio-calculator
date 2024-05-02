import { useMemo } from 'react';
import { useStore } from 'shared/store';

export const useCalculationResults = () => {
  const { appSettings, selectedRadio, customer_selection } = useStore();

  return useMemo(() => {
    const blockPositionRateValue =
      selectedRadio?.block_position_rate.find((rate) => rate.block_position.id === appSettings?.block_position?.id)
        ?.rate || 1.0;

    const seasonalRateValue = selectedRadio?.month_rate.find((rate) => rate.id === appSettings?.month?.id)?.rate || 1;

    const otherPersonRateValue =
      (appSettings?.other_person_rate && appSettings?.other_person_rate && selectedRadio?.other_person_rate) || 1;

    const hourSelectedRateeValue =
      (appSettings?.other_person_rate && appSettings?.hour_selected_rate && selectedRadio?.hour_selected_rate) || 1;

    const orderAmount = customer_selection.reduce(
      (acc, curr) =>
        acc +
        ((selectedRadio?.interval_price || []).find(
          (price) => price?.audio_duration.id === curr.audio_duration && price?.time_interval.id === curr.time_interval
        )?.interval_price || 0),
      0
    );

    const orderAmountWithRates =
      Math.round(orderAmount * blockPositionRateValue * seasonalRateValue * otherPersonRateValue) || 0;

    const amountDiscount =
      selectedRadio?.amount_discount
        .filter((discount) => orderAmountWithRates >= discount.order_amount)
        .sort((a, b) => a.order_amount - b.order_amount)
        .reverse()[0]?.discount || 0;

    const daysDiscount =
      selectedRadio?.days_discount
        .filter((discount) => [...new Set(customer_selection.map((item) => item.date))].length >= discount.total_days)
        .sort((a, b) => a.total_days - b.total_days)
        .reverse()[0]?.discount || 0;

    const volumeDiscount =
      selectedRadio?.volume_discount
        .filter((discount) => customer_selection.length >= discount.order_volume)
        .sort((a, b) => a.order_volume - b.order_volume)
        .reverse()[0]?.discount || 0;

    const totalCostValue =
      Math.round(
        orderAmountWithRates * (1 - amountDiscount / 100) * (1 - daysDiscount / 100) * (1 - volumeDiscount / 100)
      ) || 0;

    return {
      blockPositionRateValue,
      seasonalRateValue,
      otherPersonRateValue,
      hourSelectedRateeValue,
      totalCostValue,
      orderAmountWithRates,
      amountDiscount,
      daysDiscount,
      volumeDiscount
    };
  }, [customer_selection, appSettings, selectedRadio]);
};
