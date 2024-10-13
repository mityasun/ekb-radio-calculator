import { useCallback, useEffect } from 'react';
import { useStore } from 'shared/store';
import { AppSelect } from 'shared/ui/appSelect';
import { BlockPosition, AppSelectOption } from 'shared/types';
import { BLOCK_POSITION_CONTENT_TEXT, maxWidth } from '../configs';

export const PositionSelect = () => {
  const appSettings = useStore((state) => state.appSettings);
  const blockPositions = useStore((state) => state.blockPositions);
  const setBlockPosition = useStore((state) => state.setBlockPosition);
  const customer_selection = useStore((state) => state.customer_selection);

  useEffect(() => {
    if (!blockPositions) return;

    const defaultBlockPosition =
      blockPositions.find((position: BlockPosition) => position.default) || blockPositions[0];

    const isBlockPositionFound = Boolean(
      blockPositions.find((position: BlockPosition) => appSettings.block_position?.id === position.id)
    );

    if (!defaultBlockPosition || customer_selection.length > 0 || isBlockPositionFound) return;
    setBlockPosition(defaultBlockPosition);
  }, [blockPositions, customer_selection.length]);

  const options =
    blockPositions?.map((position: BlockPosition) => ({
      value: position.id.toString(),
      label: position.block_position
    })) || [];

  const getValue = useCallback(() => {
    return appSettings.block_position
      ? options.find(
          (position: AppSelectOption) => position.value.toString() === (appSettings.block_position?.id || '').toString()
        )
      : null;
  }, [appSettings, options]);

  const onChange = useCallback(
    (newValue: unknown) => {
      const selectedPosition = blockPositions?.find(
        (position: BlockPosition) => position.id.toString() === (newValue as AppSelectOption).value
      );
      if (selectedPosition) {
        setBlockPosition(selectedPosition);
      }
    },
    [blockPositions]
  );

  return (
    <AppSelect
      placeholder={!blockPositions ? BLOCK_POSITION_CONTENT_TEXT.LOADING : BLOCK_POSITION_CONTENT_TEXT.SELECT_POSITION}
      maxWidth={maxWidth}
      options={options}
      onChange={onChange}
      value={getValue()}
    />
  );
};
