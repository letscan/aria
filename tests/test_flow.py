# coding: utf-8
"""Walk around the ``Step``s
"""
from uuid import uuid4

from aria import Form, EnumField
from aria.walker import Flow, Step, FlowFinished, FlowError


class Service(object):
    """一个模拟服务器
    """
    orders = {}

    @classmethod
    def create_order(cls, params):
        order_id = uuid4()
        order = {
            'confirmed': params.get('payment') != 'online',
            'packaged': params.get('package') != 'gift',
            'delivered': False,
        }
        cls.orders[order_id] = order
        return order_id

    @classmethod
    def update_order(cls, order_id, params):
        cls.orders[order_id].update(params)

    @classmethod
    def get_order(cls, order_id):
        return cls.orders[order_id]


class SubmitOrder(Step):
    """提交订单
    """
    name = '提交订单'
    form = Form({
        'package': EnumField({'礼品包装': 'gift', '普通包装': 'standard'}),
        'payment': EnumField({'在线支付': 'online', '货到付款': 'cod'}),
    })

    def run(self, params):
        order_id = Service.create_order(params)
        order = Service.get_order(order_id)
        if order['packaged']:
            return DeliverGoods(order_id=order_id)
        elif order['confirmed']:
            return PackageGift(order_id=order_id)
        elif order:
            return OnlinePayment(order_id=order_id)
        else:
            raise FlowError('未知错误')


class OnlinePayment(Step):
    """在线支付
    """
    name = '在线支付'
    form = Form({
        'confirmed': EnumField({'确认支付': True, '取消支付': False}),
    })
    order_id = None

    def run(self, params):
        Service.update_order(self.order_id, params)
        order = Service.get_order(self.order_id)
        if order['packaged']:
            return DeliverGoods(order_id=self.order_id)
        elif order['confirmed']:
            return PackageGift(order_id=self.order_id)
        else:
            raise FlowError('订单取消')


class PackageGift(Step):
    """礼品包装
    """
    name = '礼品包装'
    form = Form({
        'packaged': EnumField({'包装成功': True, '包装失败': False}),
    })
    order_id = None

    def run(self, params):
        Service.update_order(self.order_id, params)
        order = Service.get_order(self.order_id)
        if order['packaged']:
            return DeliverGoods(order_id=self.order_id)
        elif order['confirmed']:
            return PackageGift(order_id=self.order_id)
        else:
            raise FlowError('未知错误')


class DeliverGoods(Step):
    """发货
    """
    name = '发货'
    form = Form({
        'delivered': EnumField({'妥投': True, '拒收': False}),
    })
    order_id = None

    def run(self, params):
        Service.update_order(self.order_id, params)
        order = Service.get_order(self.order_id)
        if order['delivered']:
            raise FlowFinished('订单完成')
        else:
            raise FlowError('用户拒收')


def main():
    step = SubmitOrder()
    flow = Flow(step)
    flow.walk(priority=3)

    import os
    graphviz = os.environ.get('GRAPHVIZ_PATH', 'dot')
    output_dir = os.path.realpath(os.path.join(__file__, '../../output'))
    img_path = os.path.join(output_dir, step.name + '.png')
    flow.draw(graphviz, img_path)

if __name__ == '__main__':
    main()
