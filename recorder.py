import gym, time, cv2, numpy as np, copy

class Recorder(gym.Wrapper):
    def __init__(self, env, fps = 30):
        super(Recorder, self).__init__(env)
        self.path = None
        self.video = None
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.fps = fps
    def startRecording(self, path):
        self.path = path
        frame = self.render(mode='rgb_array')
        h,w,c = frame.shape
        self.video = cv2.VideoWriter(self.path,self.fourcc, self.fps, (w,h))
        self.video.write(self.rgb2bgr(frame))
    
    def rgb2bgr(self, frame):
        temp = copy.deepcopy(frame[:,:,0])
        frame[:,:,0] = frame[:,:,2]
        frame[:,:,2] = temp
        return frame

    def recordFrame(self):
        frame = self.render(mode='rgb_array')
        frame = self.rgb2bgr(frame)
        self.video.write(frame)
    
    def endVideo(self):
        self.video.release()


if __name__ == '__main__':
    env = gym.make('CartPole-v0')
    env = Recorder(env, fps=30)

    done = False
    env.reset()

    t_start = time.time()

    # try recording 3 episodes
    for e in range(3):
        env.startRecording('videos/{}.avi'.format(e))
        done = False
        while not done:
            a = env.action_space.sample()
            obs, rew, done, info = env.step(a)
            env.recordFrame()
        env.endVideo()
        env.reset()

    env.close()
    print('time', time.time()-t_start)



