# 在 NarutoScript/agent/tests 目录下创建 test_flipping_game.py
import unittest
from unittest.mock import MagicMock, patch
from maa.context import Context
from maa.reco import RecoResult, RecoDetail
from flipping_game_action import FlippingGameAction


class TestFlippingGameAction(unittest.TestCase):
    def setUp(self):
        self.action = FlippingGameAction()
        self.context = MagicMock(spec=Context)
        self.argv = MagicMock()

    @patch("flipping_game_action.Context")
    def test_click_cards(self, mock_context):
        # 模拟识别结果
        mock_reco_detail1 = RecoDetail(x=100, y=200, width=50, height=50)
        mock_reco_detail2 = RecoDetail(x=300, y=200, width=50, height=50)

        mock_reco_result = RecoResult()
        mock_reco_result.details = [mock_reco_detail1, mock_reco_detail2]

        # 模拟 context.run_recognition 返回值
        mock_context.run_recognition.return_value = mock_reco_result

        # 模拟点击操作
        mock_controller = MagicMock()
        mock_context.tasker.controller = mock_controller

        # 测试点击逻辑
        card_patterns = ["pattern1.png", "pattern2.png"]
        self.action.click_cards(mock_context, card_patterns)

        # 验证点击次数
        self.assertEqual(mock_controller.post_click.call_count, 4)  # 两对牌，每对点击两次