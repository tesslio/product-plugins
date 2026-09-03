import { router } from '../http';
import { requireUser } from '../auth';
import { cancelOrder } from './cancel';

router.post('/orders/:id/cancel', requireUser, async (req, res) => {
  res.json(await cancelOrder(req.params.id, req.user.id));
});
