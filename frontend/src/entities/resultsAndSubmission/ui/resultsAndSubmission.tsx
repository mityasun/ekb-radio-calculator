import clsx from 'clsx';
import s from './resultsAndSubmission.module.css';
import { AppButton } from 'shared/ui/appButton';
import { getResponseOrderPdf } from 'features/getResponseOrderPDF';
import { useStore } from 'shared/store';
import { useMutation } from '@tanstack/react-query';
import { OrderPdf } from 'shared/types';
import { postOrderPdf } from '../api';
import { useCalculationResults } from 'features/useCalculationResults';
import { useState } from 'react';
import { OrderModal } from 'widgets/orderModal';
import { Tooltip } from 'react-tooltip';
import { BUTTON_TITLE, DATA_TOOLTIP_TEXT, NUMBER_DIGIT_REGEXP, RESULT_CONTENT_TEXT, toolTipStyle } from '../configs';

export type CostAndDiscounts = Record<string, { title: string; value: string | number | null; unit?: string }>;

export const ResultsAndSubmission = () => {
  const { selectedCity, appSettings, selectedRadio, customer_selection, clearCustomerSelections } = useStore();
  const [isOrderModalOpen, setOrderModalOpen] = useState<boolean>(false);
  const isDisabled = customer_selection.length === 0;

  const {
    blockPositionRateValue,
    seasonalRateValue,
    otherPersonRateValue,
    hourSelectedRateeValue,
    orderAmountWithRates,
    amountDiscount,
    daysDiscount,
    volumeDiscount,
    totalCostValue
  } = useCalculationResults();

  const costAndDiscounts: CostAndDiscounts = {
    blockPositionRate: { title: RESULT_CONTENT_TEXT.BLOCK_POSITION_RATE_TITLE, value: blockPositionRateValue },
    seasonalRate: { title: RESULT_CONTENT_TEXT.SEASONAL_RATE_TITLE, value: seasonalRateValue },
    otherPersonRate: { title: RESULT_CONTENT_TEXT.OTHER_PERSON_RATE_TITLE, value: otherPersonRateValue },
    hourSelectedRate: { title: RESULT_CONTENT_TEXT.HOUR_SELECTED_RATE_TITLE, value: hourSelectedRateeValue },
    orderAmountWithRates: {
      title: RESULT_CONTENT_TEXT.ORDER_AMOUNT_WITH_RATES_TITLE,
      value: orderAmountWithRates.toString().replace(NUMBER_DIGIT_REGEXP, ' '),
      unit: RESULT_CONTENT_TEXT.UNIT_RUB
    },
    amountDiscount: {
      title: RESULT_CONTENT_TEXT.AMOUNT_DISCOUNT_TITLE,
      value: amountDiscount,
      unit: RESULT_CONTENT_TEXT.UNIT_PRECENT
    },
    daysDiscount: {
      title: RESULT_CONTENT_TEXT.DAYS_DISCOUNT_TITLE,
      value: daysDiscount,
      unit: RESULT_CONTENT_TEXT.UNIT_PRECENT
    },
    volumeDiscount: {
      title: RESULT_CONTENT_TEXT.VOLUME_DISCOUNT_TITLE,
      value: volumeDiscount,
      unit: RESULT_CONTENT_TEXT.UNIT_PRECENT
    }
  };

  const totalCost = {
    title: RESULT_CONTENT_TEXT.TOTAL_COST_TITLE,
    value: totalCostValue.toString().replace(NUMBER_DIGIT_REGEXP, ' '),
    unit: RESULT_CONTENT_TEXT.UNIT_RUB
  };

  const mutation = useMutation<void, unknown, OrderPdf>({
    mutationFn: postOrderPdf
  });

  const handleOpenOrderModal = () => {
    setOrderModalOpen(true);
  };

  const handleCloseOrderModal = () => {
    setOrderModalOpen(false);
  };

  const hanlderSavePDFClick = async () => {
    const response = getResponseOrderPdf({ selectedCity, selectedRadio, appSettings, customer_selection });
    if (!response) return;
    mutation.mutate(response);
  };

  const handlerResetCustomerSelections = () => {
    clearCustomerSelections();
  };

  return (
    <>
      <div className={clsx(s.resultsAndSubmission)}>
        <table className={clsx(s.results)}>
          <tbody>
            {Object.keys(costAndDiscounts).map((key) => (
              <tr key={key}>
                <th>{costAndDiscounts[key as keyof typeof costAndDiscounts].title}</th>
                <td>
                  <strong>{costAndDiscounts[key as keyof typeof costAndDiscounts].value}</strong>
                  {' ' +
                    (costAndDiscounts[key as keyof typeof costAndDiscounts].unit
                      ? costAndDiscounts[key as keyof typeof costAndDiscounts].unit
                      : '')}
                </td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr>
              <th>
                <strong>{totalCost.title}</strong>
              </th>
              <td>
                <strong>{totalCost.value + ' ' + totalCost.unit}</strong>
              </td>
            </tr>
          </tfoot>
        </table>
        <div className={clsx(s.submission)}>
          <AppButton variant={'secondary'} onClick={handlerResetCustomerSelections}>
            {BUTTON_TITLE.RESET_TABLE}
          </AppButton>
          <AppButton
            variant={'secondary'}
            onClick={hanlderSavePDFClick}
            disabled={isDisabled || mutation.isPending}
            data-tooltip-id="order-button"
            data-tooltip-content={DATA_TOOLTIP_TEXT}>
            {mutation.isPending ? BUTTON_TITLE.SAVE_PDF_IS_PANDING : BUTTON_TITLE.SAVE_PDF}
          </AppButton>
          {isDisabled && <Tooltip id="order-button" place="left" style={toolTipStyle} />}
          <AppButton
            variant={'primary'}
            onClick={handleOpenOrderModal}
            disabled={isDisabled}
            data-tooltip-id="order-button"
            data-tooltip-content={DATA_TOOLTIP_TEXT}>
            {BUTTON_TITLE.SENT_TO_APROVAL}
          </AppButton>
          {isDisabled && <Tooltip id="order-button" place="left" style={toolTipStyle} />}
        </div>
      </div>
      <OrderModal isOpen={isOrderModalOpen} onClose={handleCloseOrderModal} />
    </>
  );
};
