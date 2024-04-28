import { BlockPositionRate } from 'shared/types';

export const getBlockPositions = (blockPositionRate: BlockPositionRate[]) => {
  return blockPositionRate.map((item) => {
    return {
      id: item.block_position.id,
      default: item.block_position.default,
      block_position: item.block_position.block_position
    };
  });
};
